from os import path

import argparse
import importlib
import inspect
import os
import sys
import logging

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
FAIL_COLOR = '\033[91m'
OK_COLOR = '\033[92m'
WARN_COLOR = '\033[93m'


def run_sanity_check():
    """
    Script to run a sanity check on the test cases for the GET() and POST() methods

    Args:
        test_dir (str): Path to the directory that has the test files
    """
    logger.info(
        'This script will perform a sanity test to ensure your code meets the criteria in the rubric.\n')
    logger.info(
        'Please enter the path to the file that contains your test cases for the GET() and POST() methods')
    logger.info('The path should be something like abc/def/test_xyz.py')
    filepath = input('> ')

    assert path.exists(filepath), f"File {filepath} does not exist."
    sys.path.append(path.dirname(filepath))

    module_name = path.splitext(path.basename(filepath))[0]
    module = importlib.import_module(module_name)

    test_function_names = list(filter(lambda x: inspect.isfunction(
        getattr(module, x)) and not x.startswith('__'), dir(module)))

    test_functions_for_get = list(filter(lambda x: inspect.getsource(
        getattr(module, x)).find('.get(') != -1, test_function_names))
    test_functions_for_post = list(filter(lambda x: inspect.getsource(
        getattr(module, x)).find('.post(') != -1, test_function_names))

    logger.info("\n============= Sanity Check Report ===========")
    SANITY_TEST_PASSING = True
    WARNING_COUNT = 1

    # GET()
    TEST_FOR_GET_METHOD_RESPONSE_CODE = False
    TEST_FOR_GET_METHOD_RESPONSE_BODY = False
    if not test_functions_for_get:
        logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
        WARNING_COUNT += 1
        logger.info(
            FAIL_COLOR + "No test cases were detected for the GET() method.")
        logger.info(
            FAIL_COLOR + "\nPlease make sure you have a test case for the GET method.\
            This MUST test both the status code as well as the contents of the request object.\n")
        SANITY_TEST_PASSING = False

    else:
        for func in test_functions_for_get:
            source = inspect.getsource(getattr(module, func))
            if source.find('.status_code') != -1:
                TEST_FOR_GET_METHOD_RESPONSE_CODE = True
            if (source.find('.json') != -1) or (source.find('json.loads') != -1):
                TEST_FOR_GET_METHOD_RESPONSE_BODY = True

        if not TEST_FOR_GET_METHOD_RESPONSE_CODE:
            logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
            WARNING_COUNT += 1
            logger.info(
                FAIL_COLOR +
                "Your test case for GET() does not seem to be testing the response code.\n")

        if not TEST_FOR_GET_METHOD_RESPONSE_BODY:
            logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
            WARNING_COUNT += 1
            print(
                FAIL_COLOR +
                "Your test case for GET() does not seem to be testing the CONTENTS of the response.\n")

    # POST()
    TEST_FOR_POST_METHOD_RESPONSE_CODE = False
    TEST_FOR_POST_METHOD_RESPONSE_BODY = False
    COUNT_POST_METHOD_TEST_FOR_INFERENCE_RESULT = 0

    if not test_functions_for_post:
        logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
        WARNING_COUNT += 1
        logger.info(
            FAIL_COLOR + "No test cases were detected for the POST() method.")
        logger.info(
            FAIL_COLOR +
            "Please make sure you have TWO test cases for the POST() method." +
            "\nOne test case for EACH of the possible inferences (results/outputs) of the ML model.\n")
        SANITY_TEST_PASSING = False
    else:
        if len(test_functions_for_post) == 1:
            logger.info(f"[{WARNING_COUNT}]")
            WARNING_COUNT += 1
            logger.info(
                FAIL_COLOR +
                "Only one test case was detected for the POST() method.")
            logger.info(
                FAIL_COLOR +
                "Please make sure you have two test cases for the POST() method." +
                "\nOne test case for EACH of the possible inferences (results/outputs) of the ML model.\n")
            SANITY_TEST_PASSING = False

        for func in test_functions_for_post:
            source = inspect.getsource(getattr(module, func))
            if source.find('.status_code') != -1:
                TEST_FOR_POST_METHOD_RESPONSE_CODE = True
            if (source.find('.json') != -1) or (source.find('json.loads') != -1):
                TEST_FOR_POST_METHOD_RESPONSE_BODY = True
                COUNT_POST_METHOD_TEST_FOR_INFERENCE_RESULT += 1

        if not TEST_FOR_POST_METHOD_RESPONSE_CODE:
            logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
            WARNING_COUNT += 1
            logger.info(
                FAIL_COLOR +
                "One or more of your test cases for POST() do not seem to be testing the response code.\n")
        if not TEST_FOR_POST_METHOD_RESPONSE_BODY:
            logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
            WARNING_COUNT += 1
            logger.info(
                FAIL_COLOR +
                "One or more of your test cases for POST() do not seem to be testing the contents of the response.\n")

        if len(
                test_functions_for_post) >= 2 and COUNT_POST_METHOD_TEST_FOR_INFERENCE_RESULT < 2:
            logger.info(FAIL_COLOR + f"[{WARNING_COUNT}]")
            WARNING_COUNT += 1
            logger.info(
                FAIL_COLOR +
                "You do not seem to have TWO separate test cases, one for each possible prediction that your model can make.")

    SANITY_TEST_PASSING = SANITY_TEST_PASSING and\
        TEST_FOR_GET_METHOD_RESPONSE_CODE and \
        TEST_FOR_GET_METHOD_RESPONSE_BODY and \
        TEST_FOR_POST_METHOD_RESPONSE_CODE and \
        TEST_FOR_POST_METHOD_RESPONSE_BODY and \
        COUNT_POST_METHOD_TEST_FOR_INFERENCE_RESULT >= 2

    if SANITY_TEST_PASSING:
        logger.info(OK_COLOR + "Your test cases look good!")

    logger.info(
        WARN_COLOR +
        "This is a heuristic based sanity testing and cannot guarantee the correctness of your code.")
    logger.info(
        WARN_COLOR +
        "You should still check your work against the rubric to ensure you meet the criteria.")


if __name__ == "__main__":
    run_sanity_check()
