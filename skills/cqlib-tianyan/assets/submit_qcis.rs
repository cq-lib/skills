use cqlib_tianyan::{TianyanConfig, TianyanPlatform};
use std::{env, fs, io, time::Duration};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "usage: submit_qcis BACKEND QCIS_FILE SHOTS",
        )
        .into());
    }
    let shots: usize = args[3].parse()?;
    let text = fs::read_to_string(&args[2])?;
    if shots == 0 || text.trim().is_empty() {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "positive shots and nonempty QCIS required",
        )
        .into());
    }
    let key = env::var("TIANYAN_API_KEY")?;
    let config = TianyanConfig::default().with_save_credentials(false);
    let platform = TianyanPlatform::login_with_config(&key, config)?;
    let backend = platform.get_backend(&args[1])?;
    let task = backend.run_raw(vec![text.into()], shots)?;
    println!("Submitted task IDs: {:?}", task.task_ids());
    let results = task.wait_raw(Duration::from_secs(120), Duration::from_secs(5))?;
    if results.len() != task.task_ids().len() {
        return Err(io::Error::other("result count differs from submission").into());
    }
    for (result, expected_id) in results.iter().zip(task.task_ids()) {
        if result.task_id() != expected_id {
            return Err(io::Error::other("result task ID/order mismatch").into());
        }
        println!("{} {:?}", result.task_id(), result.counts());
    }
    Ok(())
}
