ERRORS = {
    'version': 1,
    'handlers': {
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'root': {
        'handlers': ['error_handler']
    }
}

DEBUG_VERBOSE = {
}
