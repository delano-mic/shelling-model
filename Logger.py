import logging

class Logger():
    def __init__(self):
        self.setup_global_logger()

    def setup_global_logger(self):
        logger = logging.getLogger("shelling-model-logger")
        logger.setLevel(logging.INFO)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        if not logger.handlers: 
            logger.addHandler(console_handler)
   