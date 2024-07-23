#!/usr/bin/env python3

import connexion

#from connexion.options import SwaggerUIOptions
from openapi_server import encoder


def main():
    ## Connextion 2.x
    options = {
        'swagger_url': '/'
    }
    app = connexion.App(
        __name__, 
        specification_dir='./openapi/',
        options=options
    )
    
    ## Connextion 3.x
    #swagger_ui_options = SwaggerUIOptions(
    #    swagger_ui=True,
    #    swagger_ui_path='/',
    #)
    #app = connexion.App(
    #    __name__,
    #    specification_dir='./openapi/',
    #    swagger_ui_options=swagger_ui_options
    #)

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Prediction Microservice'},
                pythonic_params=True,
    )

    app.run(port=8080)


if __name__ == '__main__':
    main()
