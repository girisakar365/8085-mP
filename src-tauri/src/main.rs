#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::path::PathBuf;
use std::env;

fn main() {
// Launch the backend first
launch_backend();

// Run the Tauri app
app_lib::run()

}

fn launch_backend() {
#[cfg(target_os = "windows")]
let backend_file = "server.exe";
#[cfg(not(target_os = "windows"))]
let backend_file = "server";

// Determine backend path based on dev or production
let backend_path: PathBuf = if cfg!(debug_assertions) {
    // Development: src-tauri/resources/backend
    let exe_dir = env::current_exe()
        .expect("Failed to get current exe path")
        .parent()
        .expect("Failed to get exe directory")
        .to_path_buf();

    exe_dir
        .parent() // target
        .and_then(|p| p.parent()) // src-tauri
        .map(|p| p.join("resources").join(backend_file))
        .unwrap_or_else(|| PathBuf::from("resources").join(backend_file))
} else {
    // Production: bundled with the app
    let exe_dir = env::current_exe()
        .expect("Failed to get current exe path")
        .parent()
        .expect("Failed to get exe directory")
        .to_path_buf();

    exe_dir.join("resources").join("backend").join(backend_file)
};

if backend_path.exists() {
    Command::new(&backend_path)
        .spawn()
        .expect(&format!("Failed to start backend at {:?}", backend_path));
} else {
    eprintln!("Warning: Backend not found at {:?}", backend_path);
}

}
