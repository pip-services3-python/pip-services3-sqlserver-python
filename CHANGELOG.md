# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> SQLServer components for Python Changelog

## <a name="3.2.3-3.2.4"></a> 3.2.3-3.2.4 (2021-11-25)

### Bug fixes
* **persistence** fixed filter methods
* Fixed connection without password
* Fixed connection string compose


## <a name="3.2.2"></a> 3.2.2 (2021-11-22)

### Bug fixes
* Optimized imports
* Updated requirements

## <a name="3.2.1"></a> 3.2.1 (2021-08-29)

### Bug fixes
* Fixed config: connection, request timeouts and max pool size

## <a name="3.2.0"></a> 3.2.0 (2021-08-06)

Added support for SQL schemas

### Features
* Added schemas to SqlServerPersistence, IdentifiableSqlServerPersistence, IdentifiableJsonSqlServerPersistence
* Added _auto_generate_id flag to IdentifiableSqlServerPersistence

## <a name="3.1.0"></a> 3.1.0 (2021-05-14)

### Bug fixes
* Fixed returned types for operations

### Features
* Added type hints
* Moved SqlServerConnection to **connect** package

## <a name="3.0.0"></a> 3.0.0 (2021-03-04)

Initial public release

### Features
* Added DefaultSqlServerFactory
* Added SqlServerConnectionResolver
* Added IdentifiableJsonSqlServerPersistence
* Added IdentifiableSqlServerPersistence
* Added IndexOptions
* Added SqlServerConnection
* Added SqlServerPersistence