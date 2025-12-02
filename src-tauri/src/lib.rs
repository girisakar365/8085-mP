use std::env;

// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

/// Get the backend port that was dynamically assigned
#[tauri::command]
fn get_backend_port() -> Result<u16, String> {
    env::var("BACKEND_PORT")
        .map_err(|_| "Backend port not set".to_string())
        .and_then(|p| p.parse::<u16>().map_err(|_| "Invalid port".to_string()))
}

/// Get the full backend URL
#[tauri::command]
fn get_backend_url() -> Result<String, String> {
    let port = get_backend_port()?;
    Ok(format!("http://127.0.0.1:{}", port))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet, get_backend_port, get_backend_url])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
