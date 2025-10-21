---
name: vpn-ict-crawler
description: Crawl module information from modulbaukasten.ch
---

# VPN ICT Crawler Skill

This skill allows you to fetch detailed information about ICT modules from modulbaukasten.ch.

## Usage

When the user invokes `/crawl <module_number>`, you should:

1. Navigate to the project directory: `/home/user/ict-crawler`
2. Run the Python script to fetch module information using:
   ```bash
   python3 -c "import sys; sys.path.insert(0, '/home/user/ict-crawler'); from main import get_module_by_number; print(get_module_by_number('${MODULE_NUMBER}'))"
   ```
   Replace `${MODULE_NUMBER}` with the actual module number provided by the user.

3. Display the output to the user in a readable format.

## Example

User: `/crawl 162`

You should:
- Execute the command to fetch module 162
- Display the module details including:
  - Module number and title
  - Education program (Bildungsgang)
  - Learning location (Lernort)
  - Year (Lehrjahr)
  - Module type (Modultyp)
  - Competencies (Kompetenz)
  - PDF link if available

## Notes

- The script searches across all three education types (INF-PE, ICT, BINF)
- If the module is not found, an appropriate message will be displayed
- Make sure to handle any errors gracefully
