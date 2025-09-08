#!/usr/bin/env python3
"""
Simple script to package ErionUI source files into .mpackage format
Based on analysis of existing .mpackage structure

Usage: python3 package.py <source_dir> [version] [output_file]
Example: python3 package.py Source 1.0.4 ErionUI.1.0.4.mpackage
"""

import os
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime

def combine_xml_files(source_dir, output_path):
    """Combine separate XML files into a single Mudlet package XML"""
    
    # Read the three source files
    scripts_path = os.path.join(source_dir, "ErionUI-Scripts.xml")
    triggers_path = os.path.join(source_dir, "ErionUI-Triggers.xml") 
    keys_path = os.path.join(source_dir, "ErionUI-9Key.xml")
    
    if not all(os.path.exists(f) for f in [scripts_path, triggers_path, keys_path]):
        print("ERROR: Not all source XML files found")
        print(f"Looking for:")
        print(f"  - {scripts_path}")
        print(f"  - {triggers_path}")
        print(f"  - {keys_path}")
        return False
        
    # Parse XML files
    try:
        scripts_tree = ET.parse(scripts_path)
        triggers_tree = ET.parse(triggers_path)
        keys_tree = ET.parse(keys_path)
    except ET.ParseError as e:
        print(f"ERROR parsing XML: {e}")
        return False
    
    # Create combined XML structure
    root = ET.Element("MudletPackage", version="1.001")
    root.text = "\n"
    
    # Add triggers first (from triggers file)
    triggers_package = triggers_tree.find("TriggerPackage")
    if triggers_package is not None:
        root.append(triggers_package)
        
    # Add scripts (from scripts file)  
    scripts_package = scripts_tree.find("ScriptPackage")
    if scripts_package is not None:
        root.append(scripts_package)
        
    # Add keys (from keys file)
    keys_package = keys_tree.find("KeyPackage") 
    if keys_package is not None:
        root.append(keys_package)
    
    # Write combined XML
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t")
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
    
    print(f"Combined XML written to: {output_path}")
    return True

def create_config_lua(version="1.0.0-dev"):
    """Create config.lua with package metadata"""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    if not timestamp.endswith(('+', '-')):
        # Add timezone if not present (fallback for systems without timezone info)
        timestamp += "+00:00"
        
    config = f'''mpackage = [[ErionUI {version}]]
author = [[Caelinus]]
title = [[Minimalist Mudlet UI for ErionMud.]]
description = [[Features:
Sidebar showing important stats, event timers, and a persistent minimap.

Graphical Health and Mana bars alongside relevant combat information, including your current target and pet HP.

Chat window that keeps a record of chat whike keeping the main window clean.]]
version = [[{version}]]
created = "{timestamp}"
'''
    return config

def create_mpackage(source_dir, version="1.0.0-dev", output_file=None):
    """Create .mpackage file from source XML files"""
    
    if output_file is None:
        output_file = f"ErionUI.{version}.mpackage"
    
    # Temporary files
    combined_xml = f"/tmp/ErionUI {version}.xml"
    config_lua = "/tmp/config.lua"
    
    # Combine XML files
    print(f"Combining XML files from {source_dir}...")
    if not combine_xml_files(source_dir, combined_xml):
        return False
        
    # Create config.lua
    print("Creating config.lua...")
    with open(config_lua, 'w') as f:
        f.write(create_config_lua(version))
        
    # Create ZIP package
    print(f"Creating {output_file}...")
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(config_lua, "config.lua")
        zf.write(combined_xml, f"ErionUI {version}.xml")
    
    # Cleanup
    os.unlink(combined_xml)
    os.unlink(config_lua)
    
    print(f"Package created: {output_file}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 package.py <source_dir> [version] [output_file]")
        print("")
        print("Examples:")
        print("  python3 package.py Source")
        print("  python3 package.py Source 1.0.4")  
        print("  python3 package.py Source 1.0.4 ErionUI.1.0.4.mpackage")
        sys.exit(1)
        
    source_dir = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0-dev"
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.isdir(source_dir):
        print(f"ERROR: Source directory '{source_dir}' does not exist")
        sys.exit(1)
    
    if create_mpackage(source_dir, version, output_file):
        print("SUCCESS: Package created successfully")
        print("")
        print("To install:")
        print("1. Open Mudlet")
        print("2. Click 'Packages' on the top toolbar")
        print("3. Click 'Install New Package'")
        print(f"4. Select the created .mpackage file")
    else:
        print("ERROR: Failed to create package")
        sys.exit(1)

if __name__ == "__main__":
    main()