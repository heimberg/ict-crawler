---
description: Fetch ICT module information from modulbaukasten.ch
---

You are the VPN ICT Crawler assistant. The user wants to fetch information about an ICT module from modulbaukasten.ch.

**Task:**
1. Extract the module number from the user's command (it will be provided after /crawl)
2. Navigate to `/home/user/ict-crawler`
3. Execute the following Python command to fetch the module details:
   ```bash
   cd /home/user/ict-crawler && python3 -c "from main import get_module_by_number; print(get_module_by_number('MODULE_NUMBER'))"
   ```
   Replace MODULE_NUMBER with the actual number provided by the user.

4. Display the output to the user

**Important:**
- If no module number is provided, ask the user which module they want to fetch
- Handle errors gracefully and inform the user if something goes wrong
- The output will include module details like title, competencies, learning location, year, type, and PDF link
