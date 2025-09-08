# ErionMud-UI Development Instructions

ErionMud-UI is a Mudlet UI package for ErionMud. It consists of XML source files that define triggers, scripts, and key bindings, which are packaged into .mpackage files for distribution through Mudlet.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Quick Start - Making Changes
- Make changes to the XML files in the `Source/` directory:
  - `ErionUI-Scripts.xml` - Lua scripts and functions
  - `ErionUI-Triggers.xml` - Game triggers and text capture rules  
  - `ErionUI-9Key.xml` - Key bindings and shortcuts
- Package your changes: `python3 package.py Source <version>`
- Test in Mudlet by installing the generated .mpackage file

### Essential Commands
- **Package the UI**: `python3 package.py Source <version>` -- takes < 1 second
- **Install Mudlet (Ubuntu/Debian)**: `sudo apt update && sudo apt install mudlet` -- takes 2-5 minutes depending on connection
- **Alternative Mudlet install**: `sudo snap install mudlet --beta` -- may fail due to network restrictions

### Repository Structure
```
ErionMud-UI/
├── Source/
│   ├── ErionUI-Scripts.xml     # Lua scripts and event handlers
│   ├── ErionUI-Triggers.xml    # Text triggers and capture rules
│   └── ErionUI-9Key.xml        # Key bindings (numpad movement, etc.)
├── package.py                  # Packaging script (creates .mpackage files)
├── README.md                   # Installation instructions for end users
└── LICENSE
```

### Build and Package Process
- **NEVER CANCEL**: Packaging takes < 1 second but always complete the process
- **Command**: `python3 package.py Source [version] [output_file]`
- **Examples**:
  - `python3 package.py Source` -- creates ErionUI.1.0.0-dev.mpackage
  - `python3 package.py Source 1.0.4` -- creates ErionUI.1.0.4.mpackage
  - `python3 package.py Source 1.0.4 MyCustom.mpackage` -- creates MyCustom.mpackage
- **Output**: .mpackage file ready for distribution and Mudlet installation

### Testing Your Changes
**CRITICAL**: You MUST test in Mudlet to validate any UI changes work correctly.

1. **Install Mudlet**: `sudo apt install mudlet` (or snap/AppImage as available)
2. **Create test package**: `python3 package.py Source test-version`
3. **Install in Mudlet**:
   - Launch Mudlet
   - Click "Packages" in top toolbar
   - Click "Install New Package"
   - Select your .mpackage file
4. **Connect to ErionMud**:
   - Server: erionmud.com
   - Port: 1234
5. **VALIDATION SCENARIOS** - Always test these after making changes:
   - Login with test account and verify UI loads correctly
   - Check that sidebar shows stats properly
   - Verify chat window captures channels correctly
   - Test key bindings work (numpad movement: 8=north, 2=south, 4=west, 6=east)
   - Verify minimap displays if available
   - Test at least one trigger fires correctly when game text appears

## Development Workflow

### Making Script Changes
- Edit `Source/ErionUI-Scripts.xml`
- Look for `<Script>` elements with `<name>` tags for different functions
- Lua code is inside `<script>` CDATA sections
- **Common functions to modify**:
  - `StartUp()` - Initial UI setup
  - Event handlers for game events
  - UI positioning and layout functions

### Making Trigger Changes  
- Edit `Source/ErionUI-Triggers.xml`
- Look for `<Trigger>` elements
- Patterns are in `<regexCodeList>` elements
- Trigger actions are in `<script>` sections
- **Common triggers to modify**:
  - HP/Mana capture patterns
  - Chat channel capture
  - Combat event detection

### Making Key Binding Changes
- Edit `Source/ErionUI-9Key.xml`
- Look for `<Key>` elements
- Key codes and modifiers define which keys trigger actions
- Commands are in `<command>` elements
- **Current bindings**:
  - Numpad arrows for movement (8=north, 2=south, 4=west, 6=east, etc.)

### Release Process
1. Make and test your changes
2. Update version number when packaging: `python3 package.py Source X.Y.Z`
3. Create GitHub release with the .mpackage file as an asset
4. Update release notes with changes made

## Validation

### Pre-commit Validation
- **Always package and test** any XML changes in Mudlet before committing
- **NEVER commit** changes that haven't been tested in a live Mudlet session
- **Always verify** the .mpackage installs correctly in Mudlet
- **Manual testing required**: No automated tests exist - you must manually validate functionality

### Testing Requirements
**WARNING**: This is a UI package that requires manual testing. Simply building the package is NOT sufficient validation.

You MUST:
1. Install the package in Mudlet
2. Connect to ErionMud (erionmud.com:1234)  
3. Login and exercise the UI functionality
4. Verify all modified features work as expected
5. Check for Lua errors in Mudlet's error console

### Known Limitations
- **Cannot test without Mudlet**: The UI only works within the Mudlet client
- **Requires ErionMud connection**: Full testing requires connecting to the live game server
- **Manual validation only**: No automated testing framework exists
- **Installation required**: Changes must be packaged and installed to test

## Common Tasks

### Repository Structure Details
```bash
ls -la
# Output:
# .git/
# LICENSE            # MIT license
# README.md          # End-user installation instructions  
# Source/            # Source XML files
# package.py         # Packaging script (you may create this)
```

### Source Directory Contents
```bash  
ls -la Source/
# Output:
# ErionUI-9Key.xml      # 110 lines - Key bindings
# ErionUI-Scripts.xml   # 601 lines - Lua scripts  
# ErionUI-Triggers.xml  # 423 lines - Game triggers
```

### Typical Development Session
1. `git status` -- check current state
2. Edit XML files in Source/ directory as needed
3. `python3 package.py Source dev-test` -- create test package (< 1 second)
4. Test in Mudlet by installing the package and connecting to ErionMud
5. Iterate on changes and re-test until satisfied
6. `python3 package.py Source X.Y.Z` -- create release package with proper version
7. Create GitHub release with .mpackage file

### XML Editing Tips
- **Preserve structure**: Don't modify XML element hierarchy
- **CDATA sections**: Lua code goes in `<script><![CDATA[ code here ]]></script>`
- **Package names**: Keep `<packageName>ErionUI</packageName>` consistent
- **Test frequently**: XML syntax errors will break the entire package

### Package File Analysis
- `.mpackage` files are ZIP archives containing:
  - `config.lua` -- Package metadata (name, version, description)
  - `ErionUI <version>.xml` -- Combined XML with all triggers, scripts, and keys
- View contents: `unzip -l ErionUI.X.Y.Z.mpackage`
- Extract for inspection: `unzip ErionUI.X.Y.Z.mpackage -d /tmp/package-contents`

## Troubleshooting

### Package Creation Fails
- **Check XML syntax**: Malformed XML will cause packaging to fail
- **Verify file paths**: Ensure all three source XML files exist in Source/
- **Check permissions**: Ensure write access to current directory

### Package Installation Fails in Mudlet
- **Check file integrity**: Verify .mpackage is a valid ZIP file
- **XML validation**: Extract and check combined XML for syntax errors
- **Mudlet version**: Ensure you're using a compatible Mudlet version

### UI Doesn't Work After Installation
- **Check Lua errors**: Open Mudlet's error console for script errors
- **Verify connection**: Make sure you're connected to ErionMud (erionmud.com:1234)
- **Reload package**: Try uninstalling and reinstalling the package
- **Font issues**: May need to run the initial setup link that appears on first login

### Performance Notes
- **Packaging time**: < 1 second (never needs cancellation)
- **Mudlet startup**: 5-15 seconds depending on system
- **Package installation**: 1-2 seconds within Mudlet
- **ErionMud connection**: 2-5 seconds depending on network

Remember: This is a UI development environment focused on XML editing and manual testing rather than traditional software builds. The primary "build" step is combining XML files into a distributable package format.