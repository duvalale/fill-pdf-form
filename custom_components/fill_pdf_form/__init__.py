"""The Fill PDF Form integration."""

import logging
import os

from homeassistant.helpers import config_validation as cv
from PyPDF2 import PdfReader, PdfWriter

DOMAIN = "fill_pdf_form"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

INPUT_FILE_PATH_NAME = "input_file_path"
OUTPUT_FILE_PATH_NAME = "output_file_path"
FIELDS_DATA_NAME = "fields_data"

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_pdf_form(call):
        """Handle the service action call."""
        input_file_path = call.data.get(INPUT_FILE_PATH_NAME)
        default_output_file_path = input_file_path.replace(".pdf", "_filled.pdf")
        output_file_path = call.data.get(
            OUTPUT_FILE_PATH_NAME, default_output_file_path
        )
        updated_fields = call.data.get(FIELDS_DATA_NAME)

        hass_config_path = hass.config.config_dir
        full_input_file_path = f"{hass_config_path}{input_file_path}"
        full_output_file_path = f"{hass_config_path}{output_file_path}"

        if input_file_path is not None and os.path.exists(full_input_file_path):
            ## Retrieve fields ##
            reader = PdfReader(full_input_file_path)
            writer = PdfWriter()

            page = reader.pages[0]
            fields = reader.get_fields()

            _LOGGER.info(updated_fields)
            _LOGGER.info(fields)

            ## Fill fields and flatten file ##
            writer.add_page(page)

            writer.update_page_form_field_values(writer.pages[0], updated_fields)

            with open(full_output_file_path, "wb") as output_stream:
                writer.write(output_stream)
        else:
            _LOGGER.error(
                "'%s' is not an allowed directory or file path not provided",
                full_input_file_path,
            )

    hass.services.register(DOMAIN, "fill_pdf", handle_pdf_form)

    # Return boolean to indicate that initialization was successful.
    return True
