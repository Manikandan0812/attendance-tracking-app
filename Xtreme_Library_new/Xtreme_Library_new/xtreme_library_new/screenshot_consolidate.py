import logging
import os
import re


def get_all_files(folder_path):
    try:
        template = os.listdir(folder_path)

        files = []
        for i in template:
            image_path = os.path.join(folder_path, i)
            if os.path.isfile(image_path):
                files.append(image_path)

        files.sort(key=lambda x: [int(text) if text.isdigit() else text.lower() for text in
                                  re.split(r'(\d+)', os.path.basename(x))])
        return files
    except FileNotFoundError:
        print(f"The folder {folder_path} does not exist.")
        return []

def generate_screenshot_html(arena_dict_list, template_folder, screenshot_folder):
    """
    Generates HTML content using test case data and corresponding screenshots for each step.

    Args:
        arena_dict_list (list):
            A list of dictionaries, where each dictionary contains metadata for a test case step.
            Each entry may include fields such as:
                - 'status': Pass/Fail status of the step.
                - 'step_num': Step number or sequence.
                - 'description': Step description or action performed.
                - 'screenshot_name': Name of the screenshot file for that step.
                - Any other relevant step metadata.

        template_folder (str):
            Path to the folder containing template screenshots for each test case.
            These may be used as headers, dividers, or additional context in the generated HTML.

        screenshot_folder (str):
            Path to the folder where all the actual screenshots related to each test step are stored.
            These screenshots will be embedded or referenced in the HTML output.

    Returns:
        str:
            The generated HTML content as a string, which can be saved to a file or rendered in a browser.
    """

    step_templates = get_all_files(template_folder)
    logging.info(f"The step template datas are {step_templates}")

    numerical_templates = {}
    for template_path in step_templates:
        template_filename = os.path.basename(template_path)
        # Match only step_template_X.png where X is a number
        match = re.match(r'step_template_(\d+)\.png', template_filename)
        if match:
            step_num = match.group(1)
            # Create relative path for templates
            relative_path = f"Templates_Screens/{template_filename}"
            numerical_templates[step_num] = relative_path

    logging.info(f"Filtered numerical templates: {numerical_templates}")

    html_output_path = os.path.join(
        screenshot_folder, "screens.html")
    step_status = {}
    for data in arena_dict_list:
        step_id = data.get('STEP NUMBER', '')
        if not step_id:  # Skip entries without a step number
            continue

        status = data.get('STATUS', '')
        screenshot_link = data.get('SCREENSHOT LINK', '')

        # Extract just the filename from the screenshot path
        screenshot_filename = os.path.basename(screenshot_link) if screenshot_link else ''
        logging.info(f"The file name is {screenshot_filename}")

        if screenshot_filename.endswith(".pdf"):
            continue

        step_status[step_id] = {
            "status": "FAIL" if "FAIL" in status else "PASS" if "PASS" in status else "UNKNOWN",
            "screenshot": screenshot_filename,
        }
    logging.info(f"The step status is {step_status}")

    # HTML content for screenshot viewer
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Consolidated Screenshots</title>
 <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        #chapter-list {
            background: #f4f4f4;
            padding: 8px;
            overflow-y: auto;
            border-right: 1px solid #ddd;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
            width: 8%;
            min-width: 100px;
        }

        #chapter-list h3 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: bold;
            color: #333;
        }

        #chapter-list ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        #chapter-list li {
            margin-bottom: 6px;
            padding: 4.5px;
            cursor: pointer;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 12px;
            transition: background 0.3s, color 0.3s;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }

        #chapter-list li:hover {
            filter: brightness(90%);
            font-weight: bold;
        }

        #chapter-list li.fail {
            border-left: 4px solid #FF0000;
        }

        #chapter-list li.pass {
            border-left: 4px solid #00AA00;
        }

        #chapter-list li.intro {
            border-left: 4px solid #007bff;
        }

        /* New styles for selected state */
        #chapter-list li.selected {
            font-weight: bold;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
            z-index: 10;
        }

        #chapter-list li.selected.fail {
            background-color: #ffdddd;
            border-left: 6px solid #FF0000;
        }

        #chapter-list li.selected.pass {
            background-color: #ddffdd;
            border-left: 6px solid #00AA00;
        }

        #chapter-list li.selected.intro {
            background-color: #d1e7ff;
            border-left: 6px solid #007bff;
        }

        #chapter-list li.fail:hover {
            background-color: #ffeeee;
            border-left: 4px solid #FF0000;
            color: #000;
        }

        #chapter-list li.pass:hover {
            background-color: #eeffee;
            border-left: 4px solid #00AA00;
            color: #000;
        }

        #chapter-list li.intro:hover {
            background-color: #d1e7ff;
            border-left: 4px solid #0066cc;
            color: #000;
        }

        #chapter-list li:not(.fail):not(.pass):not(.intro):hover {
            background-color: #f4f4f4;
            color: #000;
        }

        #screenshot-container {
            flex-grow: 1;
            height: 100vh;
            overflow-y: auto;
            padding: 20px;
            background-color: #f9f9f9;
        }

        .screenshot-item {
            margin-bottom: 40px;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .screenshot-header {
            margin-bottom: 20px;
            padding: 10px 15px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 16px;
        }

        .pass-header {
            background-color: #eeffee;
            border-left: 4px solid #00AA00;
        }

        .fail-header {
            background-color: #ffeeee;
            border-left: 4px solid #FF0000;
        }

        .unknown-header {
            background-color: #f4f4f4;
            border-left: 4px solid #cccccc;
        }

        .intro-header {
            background-color: #e6f2ff;
            border-left: 4px solid #007bff;
        }

        /* Zigzag layout for images */
        .image-wrapper {
            margin-bottom: 10px;
            padding: 5px;
            background-color: #f5f5f5;
            border-radius: 6px;
            width: 95%;
            box-sizing: border-box;
        }

        .image-wrapper.left {
            margin-right: auto;
        }

        .image-wrapper.right {
            margin-left: auto;
        }

        .image-label {
            font-weight: bold;
            margin: 0 0 10px 0;
            padding: 5px 0;
            color: #444;
            border-bottom: 1px solid #ddd;
            font-size: 14px;
        }

        .screenshot-image, .template-image {
            width: 100%;
            height: auto;
            border: 1px solid #ddd;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: white;
        }

        /* For the intro section */
        #intro .image-wrapper {
            width: 95%;
            margin: 0 auto;
        }
    </style>
    </head>
    <body>
        <div id="chapter-list">
            <h3>Screenshots</h3>
            <ul>
                <li class="intro" onclick="selectChapter(this, 'intro')">
                    Intro
                </li>
    """

    # Manually build the list items one by one to avoid complex nested string formatting
    for step_id in step_status:
        status_class = step_status[step_id]["status"].lower()
        html_content += f"""
                <li class="{status_class}" onclick="selectChapter(this, 'step_{step_id}')">
                    Step {step_id}
                </li>
        """

    html_content += """
            </ul>
        </div>
        <div id="screenshot-container">
             <div id="intro" class="screenshot-item">
            <div class="screenshot-header intro-header">Introduction</div>
            <div class="image-wrapper">
                <img class="screenshot-image" src="step_intro.png" alt="Introduction Screenshot">
            </div>
        </div>
    """

    # Add each screenshot section
    for step_id in step_status:
        status_class = step_status[step_id]["status"].lower()
        screenshot = step_status[step_id]["screenshot"]

        # Find matching template for this step (if exists)
        template_path = numerical_templates.get(step_id, "")

        html_content += f"""
            <div id="step_{step_id}" class="screenshot-item">
                <div class="screenshot-header {status_class}-header">Step {step_id}</div>
        """

        # Only add template image if we have one for this step
        if template_path:
            html_content += f"""
                <div class="image-wrapper left">
                    <div class="image-label">Test Case</div>
                    <img class="template-image" src="{template_path}" alt="Template for Step {step_id}">
                </div>
            """

        html_content += f"""
                <div class="image-wrapper right">
                    <div class="image-label">Screenshot</div>
                    <img class="screenshot-image" src="{screenshot}" alt="Screenshot for Step {step_id}">
                </div>
            </div>
        """

    html_content += """
        </div>
        <script>
            function selectChapter(element, targetId) {
                // Remove 'selected' class from all list items
                const listItems = document.querySelectorAll('#chapter-list li');
                listItems.forEach(item => item.classList.remove('selected'));

                // Add 'selected' class to the clicked item
                element.classList.add('selected');

                // Scroll to the target element
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({behavior: 'smooth'});
                }
            }

            // Select the intro chapter by default when page loads
            window.onload = function() {
                const introItem = document.querySelector('#chapter-list li.intro');
                if (introItem) {
                    selectChapter(introItem, 'intro');
                }
            };
        </script>
    </body>
    </html>
    """

    # Write HTML content to file
    with open(html_output_path, "w") as html_file:
        html_file.write(html_content)

    logging.info(f"Screenshot viewer HTML generated at {html_output_path}")
    return html_output_path

