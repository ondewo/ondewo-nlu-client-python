# Release History
*****************

## Release ONDEWO NLU Python Client 2.0.0

### New Features
 * Add endpoints to list project ids, get project config and get server state to qa.proto.
 * [OND211-1799] Implement endpoints for fuzzy named entity extraction.
 * [OND211-1774] Implement endpoints to directly create/update/get/delete and list parameters.
 * [OND211-1773] Implement endpoints to directly create/update/get/delete and list responses (=intent messages).
 * [OND211-354] Establish a clear hierarchy for the merging of entities within the generalized waterfall strategy. 
   Include intent parameters to entity selection criteria.
 * [OND211-1767] Change the training phrase message to include a language_code field
 * [OND211-1766] Make training phrases endpoints work with batches.  
 * [OND211-1760] Implement endpoint to directly list training phrases.
 * [OND211-1744] Add initiation protocol into train agent endpoint
 * [OND211-1732] Implement endpoints directly create/update/get/delete training phrases.
 * [OND211-1731] Implement endpoints to directly create/update/get/delete and list entity values.
 * [OND211-1724] Add compression_level field to ExportAgentRequest message.

### Improvements
 * [OND212-29] Inject context example script added
 * [OND212-29] Full conversation demo example script added

### Migration Guide
 * `pip install ondewo-nlu-client==2.0.* --upgrade`

*****************

## Release ONDEWO NLU Python Client 1.1.2

### New Features
* added to the [pypi](https://pypi.org/project/ondewo-nlu-client/)

### Migration Guide
 * `pip install ondewo-nlu-client==1.1.2`

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
