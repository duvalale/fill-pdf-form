"""The Fill PDF Form integration."""

import logging
import os

# import datetime
import fillpdf
from fillpdf import fillpdfs

DOMAIN = "fill_pdf_form"

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
            fillpdfs.get_form_fields(full_input_file_path)

            _LOGGER.error(updated_fields)

            ## Compute fields ##
            # today = datetime.date.today()
            # last_day_of_prev_month = today.replace(day=1) - datetime.timedelta(days=1)
            # updated_fields = {
            #    "month": last_day_of_prev_month.strftime("%B %Y"),
            #    "end_of_month": last_day_of_prev_month.strftime("%d %B %Y"),
            #    "date": today.strftime("%d %B %Y"),
            # }

            ## Fill fields and flatten file ##
            fillpdfs.write_fillable_pdf(
                full_input_file_path,
                full_output_file_path,
                updated_fields,
            )
            fillpdfs.flatten_pdf(
                full_output_file_path,
                full_output_file_path,
            )
        else:
            _LOGGER.error(
                "'%s' is not an allowed directory or file path not provided",
                full_input_file_path,
            )

    hass.services.register(DOMAIN, "fill_pdf", handle_pdf_form)

    # Return boolean to indicate that initialization was successful.
    return True
