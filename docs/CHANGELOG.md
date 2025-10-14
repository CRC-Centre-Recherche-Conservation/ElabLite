# Changelog

All notable changes to ElabLite will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5-alpha] - 2025-10-13

### Added
- **Save/Save As functionality**: Users can now save experiments and create new save files
- **Auto-save system**: Automatic saving with timestamp indicators
- **Workflow stepper UI**: Visual progress bar showing current step (1-4)
- **Persistent save button**: Always-accessible save button in Steps 2-3
- **Recent saves list**: View and access 10 most recent experiment saves
- **Save validation**: Ensures required fields are filled before saving
- **Download section**: Separate download functionality for archiving
- **Save Manager module**: Centralized save operations management

### Changed
- Improved file management workflow
- Enhanced user experience with save indicators
- Better separation between working files and archives
- Updated Step 4 to focus on final export

### Fixed
- File retention in temporary directory (keeping last 10 files)
- Data persistence across page navigation
- Save path tracking in session state

## [0.1.4-alpha] - 2025-10-XX

### Added
- Enhanced dataframe editor with add/remove row functionality
- Custom technical analysis codes support
- Project configuration in base metadata

### Changed
- Improved template parsing for multiple formats
- Better error handling in file operations

## [0.1.3-alpha] - 2025-09-XX

### Added
- Support for ELABLITE custom format
- File mapping functionality
- Automatic filename generation
- ZIP export for elabFTW

### Fixed
- Template loading issues with special characters
- Unit handling in number fields

## [0.1.2-alpha] - 2025-08-XX

### Added
- Preset/template management system
- Load existing experiments feature
- Enhanced validation for emails and URLs

### Changed
- Reorganized page structure
- Improved sidebar navigation

## [0.1.1-alpha] - 2025-07-XX

### Added
- Multi-page navigation
- Form validation
- Rating and tags functionality

### Fixed
- Session state persistence issues

## [0.1.0-alpha] - 2025-06-XX

### Added
- Initial release
- Basic metadata form generation
- Template support (JSON, CSV)
- Core functionality for metadata creation
- Integration with elabFTW format

---

## Version Format

- **Major.Minor.Patch-stage**
- Stage: alpha, beta, rc (release candidate), or stable
- Example: 0.1.5-alpha

## Types of Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

**Note**: All dates in YYYY-MM-DD format. Alpha releases may have breaking changes.