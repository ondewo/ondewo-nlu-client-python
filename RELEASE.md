# Release History
*****************

## Release ONDEWO NLU Python Client 1.1.2

### New Features
* added to the [pypi](https://pypi.org/project/ondewo-nlu-client/)

### Migration Guide
 * pip install ondewo-nlu-client==1.1.2

*****************

## Release ONDEWO NLU Python Client 1.1.1

### New Features
* py2 compatibility

*****************

## Release ONDEWO NLU Python Client 1.1.0

### New Features
 Implemented new endpoints:
 * [OND211-1693] Implement regex validation endpoints.
 * [OND211-1714] Implement intent cleaning endpoints.
 * [OND211-1714] Implement entity_type cleaning endpoints.
 * [OND211-1714] Implement endpoints to add new training phrases to intents.

*****************
## Release ONDEWO NLU Python Client 1.0.1

### Improvements
 * Add convenient Make targets for easier development

### Bug fixes
 * Fix the setup.py configuration

### Known issues not covered in this release
 * CI/CD Integration is missing
 * Code Quality checks
 * Extend the README.md with an examples usage

*****************

## Release ONDEWO NLU Python Client 1.0.0

### New Features
 * First public version

### Improvements
 * Open source

### Breaking Changes
 * Type definition for Parameters improved (`context.proto`)

### Known issues not covered in this release
 * CI/CD Integration is missing
 * Code Quality checks
 * Extend the README.md with an examples usage

### Migration Guide
 * Usages of the Context Parameters must be adapted to the new typed structure
