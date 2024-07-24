import sys
import os
import time
from helpers.java_helpers import generate_java_source, compile_java_class, get_trace_xml, get_all_method_names
from helpers.input_parser import get_inputs

# Global variable for max retries
MAX_RETRIES = 3
COUNTER = 0

# Function to compile Java source code and run JBMC
def compile_and_run_jbmc(jbmc_path, file_path, filename, unwind_limit):
    """
    Compiles the Java source code and runs JBMC to obtain trace XML source.

    Args:
        jbmc_path (str): Path to the JBMC executable.
        file_path (str): Path to the Java source file.
        filename (str): Name of the Java source file.
        unwind_limit (int): Unwind limit for JBMC.
        extra_jbmc_options (str): Extra JBMC Options.

    Returns:
        list: List of tuples containing method names and trace XML sources.
    """
    # Compile Java source code
    print('Compiling Java source...')
    compile_java_class(file_path)

    # Run JBMC and get trace XML source with specified unwind limit
    print('Running JBMC...')
    # Simple loading animation
    start_time = time.time()
    animation_chars = "/—\|"
    while True:
        elapsed_time = time.time() - start_time
        for char in animation_chars:
            sys.stdout.write(f'\r{char} Running JBMC... Elapsed Time: {int(elapsed_time)}s')
            sys.stdout.flush()
            time.sleep(0.1)
            if elapsed_time > 2:  
                break
        if elapsed_time > 2:
            break
    sys.stdout.write('\r' + ' ' * 50 + '\r')  # Clear the loading animation

    methods = get_all_method_names(file_path)
    trace_xml_source_list = []

    for method in methods:
        trace_xml_source = get_trace_xml(
            jbmc_path,
            filename,
            method,
            ['--unwind', str(unwind_limit), "-cp", "../../lib/core-models.jar:../../lib/cprover-api.jar:."]
        )

        trace_xml_source_list.append((method, trace_xml_source))


    return trace_xml_source_list

# Function to generate Java counterexample source files
def generate_counterexamples(filename, method_name, counterexample_inputs):
    """
    Generates Java counterexample source files based on the trace XML sources.

    Args:
        filename (str): Name of the Java source file.
        method_name (str): Name of the method associated with the counterexample.
        counterexample_inputs (dict): Counterexample inputs and reason.
    """
    global COUNTER
    for i, counterexample_input in enumerate(counterexample_inputs):
        reason = counterexample_input['reason']
        inputs = counterexample_input['inputs']
        out_class_name = f'CounterExample{COUNTER}'
        COUNTER = COUNTER + 1

        # Generate Java counterexample source code
        print(f'Generating Java counterexample source ({i + 1}/{len(counterexample_inputs)}) for method: {method_name} ...')
        source = generate_java_source(
            test_class_name=filename,
            out_class_name=out_class_name,
            counterexample_inputs=inputs, reason=reason,
            method_name = method_name
        )

        # Write the generated source code to a file
        with open(out_class_name + '.java', 'w') as file:
            file.write(source)

# Function to display JBMC result
def display_jbmc_result(counterexample_count):
    """
    Displays the result of JBMC execution.

    Args:
        counterexample_count (int): Number of counterexamples produced by JBMC.
    """
    if counterexample_count == 0:
        print('JBMC was successful, no CounterExamples produced!')
    else:
        print(f'JBMC Check Failed, {counterexample_count} counterexamples produced.')

    print('DONE')

# Main function
def main(argv):
    """
    Main function to orchestrate the execution flow.

    Args:
        argv (list): List of command-line arguments.
    """
    # Get JBMC path, Java file path, and filename from command-line arguments
    retry_count = 0

    while retry_count < MAX_RETRIES:
        jbmc_path = argv[1] or './jbmc'
        file_path = argv[2]
        filename = file_path.split('.')[0]

        # Check if the JBMC path is correct
        if not os.path.isfile(jbmc_path):
            print(f'Error: The specified JBMC file path "{jbmc_path}" is not valid.')

            # Prompt for re-entry
            jbmc_path = input('Please enter the correct path to JBMC: ')
            retry_count += 1

            # Check again after re-entering the path
            if os.path.isfile(jbmc_path):
                break
            else:
                print(f'Error: Still an invalid JBMC file path. Retrying ({retry_count}/{MAX_RETRIES})...')

        else:
            break  # JBMC path is valid, exit the retry loop

    # If max retries reached and the path is still invalid, exit
    if retry_count == MAX_RETRIES and not os.path.isfile(jbmc_path):
        print('Error: Exceeded maximum retries. Exiting.')
        sys.exit(1)

    # Ask the user for the unwind limit or use the default value
    unwind_limit = get_unwind_limit_from_user()

    # Compile Java source code and run JBMC, get trace XML source
    trace_xml_source_list = compile_and_run_jbmc(jbmc_path, file_path, filename, unwind_limit)

    # Parse counterexamples from trace XML source
    print('Parsing counterexamples...')
    counterexample_inputs = []
    for method, trace_xml_source in trace_xml_source_list:
        counterexample_input = get_inputs(trace_xml_source)
        counterexample_inputs.append((method, counterexample_input))
        generate_counterexamples(filename, method, counterexample_input)

    # Display JBMC result
    display_jbmc_result(COUNTER)

# Function to get user input for the unwind limit
def get_unwind_limit_from_user():
    """
    Prompts the user to enter the unwind limit.

    Returns:
        int: Unwind limit specified by the user.
    """
    default_value = 10
    retries = 0

    while retries < MAX_RETRIES:
        try:
            user_input = input(f'Enter unwind limit (default is {default_value}, press Enter to keep default): ')
            if not user_input:  # Enter pressed, use the default value
                return default_value

            unwind_limit = int(user_input)
            if unwind_limit <= 0:
                print('Unwind limit must be greater than 0. Try again.')
                retries += 1
            else:
                return unwind_limit
        except ValueError:
            print('Invalid input. Please enter a number greater than 0. Try again.')
            retries += 1

    # If the user has exceeded the maximum number of retries, use the default value
    print(f'Exceeded maximum retries. Using default value ({default_value}).')
    return default_value

# Entry point of the script
if __name__ == '__main__':
    # Call the main function with command-line arguments
    main(sys.argv)
