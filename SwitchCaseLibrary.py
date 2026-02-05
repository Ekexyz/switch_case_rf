from typing import Any, Callable, Dict, List, Optional, Union
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

@library(scope='GLOBAL', auto_keywords=True)
class SwitchCaseLibrary:

    """
    This library allows you to define a mapping of values to keywords and
    their arguments, then execute the appropriate keyword based on a switch
    value.

    Example usage in Robot Framework:

    | *** Settings ***
    | Library    SwitchCaseLibrary
    |
    | *** Test Cases ***
    | Example Test With Switch Case
    |     ${result}=    Switch Case    apple
    |     ...    apple=Log    message=Found an apple!
    |     ...    banana=Log    message=Found a banana!
    |     ...    orange=Log    message=Found an orange!
    |     ...    default=Log    message=Unknown fruit
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    def __init__(self) -> None:
        """Initialize the SwitchCaseLibrary."""
        self.builtin = BuiltIn()

    @keyword("Run Keyword Switch")
    def run_keyword_switch(
        self,
        switch_value: Any,
        case_map: Dict[str, Union[str, List[str]]]
    ) -> Any:
        """
        Execute a keyword using a dictionary for case mappings.

        Alternative implementation using a dictionary for case mappings.
        Useful when you want to define cases programmatically or in variables.

        Args:
            switch_value: The value to match against case definitions
            case_map: Dictionary mapping case values to keyword definitions

        Returns:
            The return value from the executed keyword (if any)

        Raises:
            TypeError: If case_map is not a dictionary
            ValueError: If no matching case is found and no default exists

        Example:
        | ${cases}=    Create Dictionary
        | ...    case1=Log    First case
        | ...    case2=Log    Second case
        | ...    default=Log    Default case
        | Run Keyword Switch    case1    ${cases}
        """
        if not isinstance(case_map, dict):
            raise TypeError(
                f"case_map must be a dictionary, got {type(case_map).__name__}"
            )

        switch_str = str(switch_value)

        if switch_str in case_map:
            case_definition = case_map[switch_str]
        elif 'default' in case_map:
            case_definition = case_map['default']
        else:
            raise ValueError(
                f"No matching case found for '{switch_value}' and no "
                f"default case defined"
            )

        return self._execute_case(case_definition)

    def _execute_case(
        self,
        case_definition: Union[str, List[str], tuple]
    ) -> Any:
        """
        Parse and execute a case definition.

        Internal method to parse and execute a case definition in various
        formats.

        Args:
            case_definition: String containing keyword name and optional
                arguments separated by spaces, or a list/tuple
                [keyword, arg1, arg2, ...]

        Returns:
            The return value from the executed keyword

        Raises:
            ValueError: If case definition is empty
            TypeError: If case definition type is invalid
        """
        # Handle list/tuple format: ['keyword', 'arg1', 'arg2']
        if isinstance(case_definition, (list, tuple)):
            if not case_definition:
                raise ValueError("Case definition list cannot be empty")

            keyword_name = case_definition[0]
            args = list(case_definition[1:])
            logger.console(f'run_kw: {keyword_name} with args: {args}')
            return self.builtin.run_keyword(keyword_name, *args)

        # Handle string format: "keyword arg1 arg2"
        if isinstance(case_definition, str):
            parts = case_definition.split(maxsplit=1)
            keyword_name = parts[0]

            # Parse arguments if present
            if len(parts) > 1:
                # Simple split by spaces - for complex args, use list format
                args = parts[1].split()
                logger.console(f'run_kw: {keyword_name} with args: {args}')
                return self.builtin.run_keyword(keyword_name, *args)
            else:
                return self.builtin.run_keyword(keyword_name)

        raise TypeError(
            f"Case definition must be a string or list, "
            f"got {type(case_definition).__name__}"
        )
