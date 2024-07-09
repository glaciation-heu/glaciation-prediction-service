#!/usr/bin/env python3

import connexion

from openapi_server import encoder


def main():
    options = {
        'openapi_spec_path': '/ui/openapi.json'
    }
    app = connexion.App(
        __name__, 
        specification_dir='./openapi/',
        options=options
    )
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Prediction Microservice'},
                pythonic_params=True,
    )

    app.run(port=8080)


if __name__ == '__main__':
    main()
