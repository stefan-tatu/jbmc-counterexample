from subprocess import run
from typing import Optional

def get_trace_xml(jbmc_path: str, class_name: str, options: Optional[list] = None) -> str:
    """
    Run JBMC tool to generate XML trace for the given Java class.

    Args:
        jbmc_path (str): The path to the JBMC tool.
        class_name (str): The name of the Java class.
        options (list, optional): Additional options for the JBMC command. Defaults to None.

    Returns:
        str: The XML trace generated by JBMC.
    """
    assert options is None or len(options) > 0

    cmd = [jbmc_path, f'{class_name}.test', '--xml-ui']
    if options is not None:
        cmd.extend(options)
    
    # Run JBMC command and capture the output
    result = run(cmd, capture_output=True, text=True)
    return result.stdout

