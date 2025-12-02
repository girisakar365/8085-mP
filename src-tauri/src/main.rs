#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Child};
use std::path::PathBuf;
use std::env;
use std::net::TcpListener;
use std::sync::Mutex;
use std::time::Duration;
use std::thread;

// Global backend process handle for lifecycle management
static BACKEND_PROCESS: Mutex<Option<Child>> = Mutex::new(None);

fn main() {
    // Find available port and launch backend
    let port = find_available_port(8085, 9000).unwrap_or(8085);
    
    // Set port as environment variable for frontend to discover
    env::set_var("BACKEND_PORT", port.to_string());
    
    // Launch the backend with the selected port
    launch_backend(port);
    
    // Give backend time to start
    thread::sleep(Duration::from_millis(1500));
    
    // Verify backend is running
    if !check_backend_health(port) {
        eprintln!("Warning: Backend health check failed. The application may not work correctly.");
    }
    
    // Run the Tauri app
    app_lib::run();
    
    // Cleanup: Stop backend when app exits
    shutdown_backend();
}

/// Find an available port in the given range
fn find_available_port(start: u16, end: u16) -> Option<u16> {
    for port in start..end {
        if TcpListener::bind(format!("127.0.0.1:{}", port)).is_ok() {
            println!("Found available port: {}", port);
            return Some(port);
        }
    }
    eprintln!("No available port found in range {}-{}", start, end);
    None
}

/// Check if backend is responding
fn check_backend_health(port: u16) -> bool {
    for attempt in 1..=5 {
        match std::net::TcpStream::connect_timeout(
            &format!("127.0.0.1:{}", port).parse().unwrap(),
            Duration::from_millis(500)
        ) {
            Ok(_) => {
                println!("Backend health check passed on attempt {}", attempt);
                return true;
            }
            Err(_) => {
                if attempt < 5 {
                    thread::sleep(Duration::from_millis(300));
                }
            }
        }
    }
    false
}

/// Get the backend binary path based on platform and install type
fn get_backend_path() -> Option<PathBuf> {
    #[cfg(target_os = "windows")]
    let backend_file = "server.exe";
    #[cfg(not(target_os = "windows"))]
    let backend_file = "server";

    let product_name = "ASM STUDIO"; // Must match tauri.conf.json

    let mut candidates: Vec<PathBuf> = Vec::new();

    if let Ok(exe_path) = env::current_exe() {
        println!("Executable path: {:?}", exe_path);
        
        if let Some(exe_dir) = exe_path.parent() {
            println!("Executable directory: {:?}", exe_dir);

            if cfg!(debug_assertions) {
                // Development: src-tauri/resources/backend
                if let Some(src_tauri_dir) = exe_dir.parent().and_then(|p| p.parent()) {
                    candidates.push(src_tauri_dir.join("resources").join("backend").join(backend_file));
                }
                // Also try current working directory
                candidates.push(PathBuf::from("resources").join("backend").join(backend_file));
            } else {
                // Production paths

                // 1. AppImage: /tmp/.mount_xxx/usr/bin/app -> resources in /tmp/.mount_xxx/usr/lib/<ProductName>/resources/backend/
                if let Some(usr_dir) = exe_dir.parent() {
                    if let Some(mount_dir) = usr_dir.parent() {
                        candidates.push(
                            mount_dir
                                .join("usr")
                                .join("lib")
                                .join(product_name)
                                .join("resources")
                                .join("backend")
                                .join(backend_file)
                        );
                    }
                }

                // 2. Relative to executable (Windows, some Linux setups)
                candidates.push(exe_dir.join("resources").join("backend").join(backend_file));

                // 3. macOS .app bundle: Contents/MacOS/app -> Contents/Resources/backend/
                #[cfg(target_os = "macos")]
                if let Some(contents_dir) = exe_dir.parent() {
                    candidates.push(
                        contents_dir
                            .join("Resources")
                            .join("backend")
                            .join(backend_file)
                    );
                }

                // 4. System-wide install (.deb/.rpm): /usr/lib/<ProductName>/resources/backend/
                #[cfg(target_os = "linux")]
                {
                    candidates.push(PathBuf::from(format!(
                        "/usr/lib/{}/resources/backend/{}",
                        product_name, backend_file
                    )));
                    // Also try without spaces (some distros)
                    candidates.push(PathBuf::from(format!(
                        "/usr/lib/{}/resources/backend/{}",
                        product_name.replace(' ', "-"), backend_file
                    )));
                    candidates.push(PathBuf::from(format!(
                        "/usr/lib/{}/resources/backend/{}",
                        product_name.replace(' ', "_").to_lowercase(), backend_file
                    )));
                }
            }
        }
    }

    // Debug: print all candidate paths
    println!("Searching for backend binary in {} locations:", candidates.len());
    for (i, path) in candidates.iter().enumerate() {
        let exists = path.exists();
        println!("  [{}] {:?} - {}", i + 1, path, if exists { "EXISTS" } else { "not found" });
    }

    // Return the first existing path
    candidates.into_iter().find(|path| path.exists())
}

/// Launch the backend process
fn launch_backend(port: u16) {
    let backend_path = match get_backend_path() {
        Some(path) => path,
        None => {
            eprintln!("Error: Backend binary not found in any known location.");
            eprintln!("Please ensure the backend is properly bundled with the application.");
            return;
        }
    };

    println!("Starting backend at {:?} on port {}", backend_path, port);

    let child = Command::new(&backend_path)
        .env("BACKEND_PORT", port.to_string())
        .env("TAURI_ENV", "1")
        .spawn();

    match child {
        Ok(process) => {
            println!("Backend started successfully (PID: {})", process.id());
            
            // Store process handle for lifecycle management
            if let Ok(mut guard) = BACKEND_PROCESS.lock() {
                *guard = Some(process);
            }
        }
        Err(e) => {
            eprintln!("Failed to start backend at {:?}: {}", backend_path, e);
            eprintln!("Error details: {:?}", e.kind());
        }
    }
}

/// Gracefully shutdown the backend process
fn shutdown_backend() {
    if let Ok(mut guard) = BACKEND_PROCESS.lock() {
        if let Some(mut process) = guard.take() {
            println!("Shutting down backend process...");
            
            // Force kill if still running
            match process.try_wait() {
                Ok(Some(status)) => println!("Backend exited with status: {}", status),
                Ok(None) => {
                    println!("Backend still running, forcing shutdown...");
                    let _ = process.kill();
                    let _ = process.wait();
                    println!("Backend forcefully terminated.");
                }
                Err(e) => eprintln!("Error checking backend status: {}", e),
            }
        }
    }
}