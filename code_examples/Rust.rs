#![allow(dead_code)]

/// Doc comment
//! Doc comment
// Normal comment
#[derive(Debug, Clone)]
#[repr(C)]
struct User<'a, T>
where
    T: Clone + Send,
{
    name: &'a str,
    value: Option<T>,
}

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

const MAX: usize = 0xff;
static mut COUNTER: i32 = 0;

enum State {
    Idle,
    Running(u32),
    Failed { code: i32 },
}

trait Displayable {
    fn display(&self) -> String;
}

impl<T: std::fmt::Debug> Displayable for User<'_, T> {
    fn display(&self) -> String {
        format!("{:?}", self)
    }
}

fn process<'a>(
    input: &'a str,
    mut values: Vec<i32>,
) -> Result<Option<&'a str>> {
    let tuple: (i32, bool) = (42, true);

    let mut map = std::collections::HashMap::new();
    map.insert("key", None::<String>);

    let closure = |x: i32| x * 2;

    for value in &mut values {
        *value += closure(*value);
    }

    match tuple {
        (number, true) if number > 0 => println!("{number}"),
        (_, false) => {}
        _ => unreachable!(),
    }

    let text = format!(
        "value={:?}, hex={:#x}",
        tuple,
        MAX
    );

    let raw = r#"raw "string" "#;
    let bytes = b"bytes";
    let byte_char = b'A';

    if let Some(item) = map.get("key") {
        return Ok(item.as_deref());
    }

    Ok(Some(input))
}

async fn fetch() -> Result<()> {
    let value = async { 42 }.await;

    unsafe {
        COUNTER += value;
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn example() {
        assert_eq!(1 + 1, 2);
    }
}
