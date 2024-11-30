# fill-pdf-form
This is a custom component for Home Assistant. This integration allows to fill a PDF Form thanks to a home assistant service.

## Installation

Clone the content of custom_components/fill_pdf_form from this repo into the custom_components directory:


## Configuration

Home Assistant must first be allowed to access the directory with the target PDF file.

Add the allowlist_external_dirs to configuration.yaml. In this example, the PDF exists at /config/my.pdf:

```
homeassistant:
  allowlist_external_dirs:
    - /config
```

Next add the integration to the configuration.yaml:

```
sensor:
  - platform: pdf
    name: My PDF Sensor
    file_path: /config/my.pdf
```

## How to use

A new service fill_pdf_form.fill_pdf is now available.

Please not that you must know the name of the fields to fill, or you can find them by setting log level to info.

An example of how to call the service (the PDF is still in /config/my.pdf) :

```
action: fill_pdf_form.fill_pdf
data:
  input_file_path: '/my.pdf'
  output_file_path: '/filled.pdf'
  fields_data: { 'month': 'test' }
```