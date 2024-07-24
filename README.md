# JBMC Counterexample Generator

This utility facilitates generating counterexamples for Java programs utilizing the Java Bounded Model Checker (JBMC). It automates Java source code compilation, JBMC execution, and trace XML extraction to produce counterexample Java files.

## Prerequisites

Before using this tool, ensure the following are installed:

- Python 3.x
- Java Development Kit (JDK)
- JBMC

## Installation

To set up the JBMC Counterexample Generator:

1. Clone or download this repository to your machine.
2. Ensure the `jbmc-counterexample.py` script is within the `src` directory.
3. Place your Java file for analysis within the `code_verification/<YourAppName>` directory, where `<YourAppName>` should be replaced with the name of your application or project.

## Usage

To execute the script, you must be inside the `code_verification/<YourAppName>` directory:

1. Change to your specific application directory: `code_verification/<YourAppName>`.
2. Run the script with the following command, ensuring to replace `<jbmc_full_path>` with the path to your JBMC installation and `<YourJavaFile.java>` with the name of your Java file:

    ```bash
    python3 ../../src/jbmc-counterexample.py <jbmc_full_path> <YourJavaFile.java>
    ```

**Note:** `<YourAppName>` and `<YourJavaFile.java>` are placeholders. You should replace `<YourAppName>` with your directory name and `<YourJavaFile.java>` with your Java file's name. For example, if your application name is `MyApp` and your Java file is `Test.java`, the directory would be `code_verification/MyApp`, and the command would look like this:

    ```bash
    python3 ../../src/jbmc-counterexample.py /path/to/jbmc `<YourJavaFile.java>
    ```

### Directory Structure

Ensure your project adheres to the following structure:

- `code_verification/`: Contains application-specific folders for verification processes.
- `<YourAppName>`: Directory named after your application, holding the Java file for analysis.
- `src/`: Contains the script `jbmc-counterexample.py`.
- `libs/`: Containing cprover libs needed for the wrapper.

## Output

Upon execution, Java source files representing counterexamples are generated and placed in the `code_verification/<YourAppName>` directory, named as `CounterExample<N>.java`.
