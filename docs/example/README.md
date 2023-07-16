# Example Project using OCE Build

This is a simple project that showcases an example project structure and build configuration format and the various commands available in OCE Build. This is isn't meant to be a comprehensive example, but rather a simple example to test the CLI and build system.

You can see a list of all available commands by running `poetry run ocebuild -h` or `ocebuild -h`. For help with an individual command, run `poetry run ocebuild <command> -h` or `ocebuild <command> -h`.

For example, to run the build system, run the following command:

```sh
$ poetry run ocebuild build --cwd docs/example
# Or
$ ocebuild --cwd docs/example
```

Or to run the lock command, run:

```sh
$ poetry run ocebuild lock --cwd docs/example
# Or
$ ocebuild lock --cwd docs/example
```
