import logging
import os
import re
import time
from babel.dates import format_time
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips


def format_time(seconds):
    """Formats seconds as MM:SS."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{str(minutes).zfill(2)}:{str(secs).zfill(2)}"


def video_consolidate(list_data, video_links, template_folder, video_folder, video_width=1920, video_height=1080):
    """
      Consolidates multiple test case videos into a single video with optional template screenshots between them.

      Args:
          list_data (list):
              A list of dictionaries, where each dictionary contains metadata for a test case.
              Each entry may include fields such as:
                  - 'status': Pass/Fail status of the test case.
                  - 'step_num': Step number or sequence.
                  - 'start_time': Timestamp when the test case started.
                  - 'end_time': Timestamp when the test case ended.
                  - 'duration': Duration of the test case execution.
                  - Any other relevant test metadata.

          video_links (list):
              A list of absolute file paths to the test case videos that need to be consolidated.

          template_folder (str):
              Path to the folder containing template screenshots to be inserted
              between video clips (e.g., start/end screens, separators).

          video_folder (str):
              Destination folder path where the final consolidated video will be saved.

          video_width (int, optional):
              Width of the output video in pixels. Defaults to 1920.

          video_height (int, optional):
              Height of the output video in pixels. Defaults to 1080.

      Returns:
          None
      """
    logging.info("The video consolidation started ..")

    clips = []
    step_templates = template_folder
    list_data.sort(key=lambda x: int(x["STEP NUMBER"]))
    consolidate_path = os.path.join(video_folder, "consolidate_video.webm")
    html_output_path = os.path.join(video_folder, "video_player.html")

    if step_templates:
        introduction_image = step_templates[0]
        if os.path.exists(introduction_image):
            intro_clip = ImageClip(introduction_image, duration=4).resize((video_width, video_height))
            clips.append(intro_clip)  # Resize image to 1920x1080
        else:
            logging.warning(f"Introduction image not found: {introduction_image}")

    chapter_start_times = []
    current_time = 0
    chapter_start_times.append((current_time, "Intro"))

    for i, (video, image) in enumerate(zip(video_links, step_templates[1:]), start=1):
        video_path = video
        screenshot_path = image
        logging.info(f"Processing step {i}: {screenshot_path}, {video_path}")

        # Add image clip
        if os.path.exists(screenshot_path):
            image_clip = ImageClip(screenshot_path, duration=4).resize((video_width, video_height))
            clips.append(image_clip)
            current_time += 4  # Image clip duration

        # Add video clip
        if os.path.exists(video_path):
            video_clip = VideoFileClip(video_path).resize((video_width, video_height))
            clips.append(video_clip)
            chapter_start_times.append((current_time, f"Step {i}"))
            current_time += video_clip.duration
        else:
            logging.warning(f"Video not found: {video_path}")

    # Combine clips into a single video
    if clips:
        try:
            final_clip = concatenate_videoclips(clips, method="compose")
            final_clip.write_videofile(
                consolidate_path,
                fps=1,
                codec="vp8",
                preset="fast",
                ffmpeg_params=["-pix_fmt", "yuv420p"],
            )
            logging.info(f"Video saved to {consolidate_path}")

            # Generate HTML file
            step_html_files, consolidate_video_html_relpath = generate_html_files(list_data, consolidate_path,
                                                                                  chapter_start_times, html_output_path)
            time.sleep(1)

            return consolidate_video_html_relpath, step_html_files

        except Exception as e:
            logging.error(f"Error creating consolidated video: {e}")
    else:
        logging.warning("No valid clips to combine.")
        return None


def generate_html_files(data_dict_list, video_path, chapters, html_base_path):
    """Generates multiple HTML files - a main player and separate files for each step."""
    video_clip = VideoFileClip(video_path)
    total_duration = video_clip.duration
    video_folder = os.path.dirname(html_base_path)

    # Create a dictionary to map step titles to their status
    step_status = {}
    for data in data_dict_list:
        step_id = data.get('STEP NUMBER', '')
        status = data.get('STATUS', '')

        # Extract step number from title if it exists
        for start_time, title in chapters:
            if f"step_{step_id}" in title.lower() or f"step {step_id}" in title.lower():
                step_status[title] = "FAIL" if "FAIL" in status else "PASS"

    # Convert chapters to JSON for JavaScript with status information
    chapters_json = []
    for start_time, title in chapters:
        status = step_status.get(title, "UNKNOWN")
        chapters_json.append({
            "start_time": start_time,
            "title": title,
            "status": status
        })

    # Main HTML content (same as before)
    html_content = generate_player_html(video_path, total_duration, chapters, step_status, chapters_json)

    # Write main HTML content to file
    with open(html_base_path, "w") as html_file:
        html_file.write(html_content)
    logging.info(f"Main HTML player generated at {html_base_path}")

    step_files = []
    for i, (start_time, title) in enumerate(chapters):
        step_match = re.search(r'step[_\s]*(\d+)', title, re.IGNORECASE)
        if step_match:
            step_id = step_match.group(1)
        else:
            step_id = str(i + 1)  # Use index+1 if no explicit step number found

        step_html_path = os.path.join(video_folder, f"step_{step_id}.html")

        redirect_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="0;url={os.path.basename(html_base_path)}?step={title}">
            <title>Redirecting to {title}</title>
        </head>
        <body>
            <p>Redirecting to <a href="{os.path.basename(html_base_path)}?step={title}">{title}</a>...</p>
        </body>
        </html>
        """

        with open(step_html_path, "w") as step_file:
            step_file.write(redirect_html)

        logging.info(f"Step HTML file generated at {step_html_path}")
        step_files.append(step_html_path)

    return html_base_path, step_files


def generate_player_html(video_path, total_duration, chapters, step_status, chapters_json):
    """Generates the HTML content for the video player."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arena Automation</title>
         <style>
             body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        height: 100vh;
        overflow: hidden;
    }}

            #video-container {{
                position: relative;
                width: 85%;
                margin: auto;
                max-height: calc(100vh - 50px); /* Maximum height to fit screen */
                display: flex;
                flex-direction: column;
                transition: all 0.3s ease-in-out; /* Smooth transition */
            }}
            video {{
                width: 100%;
                height: auto; /* Maintain aspect ratio */
                max-height: calc(100vh - 120px); /* Ensure progress bar and controls are visible */
            }}
            #progress-bar-container {{
                position: relative;
                width: 100%;
                height: 5px;
                background: #ddd;
                cursor: pointer;
                margin-top: 25px;
            }}
            #progress-bar {{
                position: absolute;
                height: 100%;
                background: #F05959; /* Light red fill */
                width: 0%;
            }}
            #play-button {{
                font-size: 11px;
                padding: 5px 10px;
                border: none;
                background-color: #007bff;
                color: #fff;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 12px;
            }}
            #play-button:hover {{
                background-color: #0056b3;
            }}
            .chapter-marker {{
                position: absolute;
                height: 100%;
                width: 2px;
                background: #000000;
                cursor: pointer;
            }}

            #controls {{
                display: flex;
                justify-content: space-between; /* Align items left and right */
                align-items: center;
                width: 100%;
                margin-top: 10px;
            }}
            #controls-left {{
                display: flex;
                align-items: center;
                justify-content: flex-start;
                flex: 1;
                margin-top: -12px ;
            }}
            #time-display {{
                font-size: 13px;
                margin-top: 12px;
                margin-left: 12px;
                margin-right: 12px;
            }}
            .chapter-marker {{
    position: absolute;
    height: 100%;
    width: 2px;
    background: #000000; /* Default black color for all markers */
    cursor: pointer;
}}
            #current-step {{
                font-size: 13px;
                font-weight: bold;
                margin-top: 12px;
                padding: 3px 8px;
                border-radius: 4px;
            }}
            /* Status color classes for the current step text */
            .step-status-fail {{
                background-color: #ffeeee;
                color: black;
                border: 1px solid #ff0000;
            }}
            .step-status-pass {{
                background-color: #eeffee;
                color: black;
                border: 1px solid #00aa00;
            }}
            #chapter-list li:hover {{
    filter: brightness(90%); /* Subtle darkening effect instead of blue */
    font-weight: bold;
}}
            .step-status-unknown {{
                background-color: #f4f4f4;
                color: black;
                border: 1px solid #cccccc;
            }}
            #chapter-list li.fail:hover {{
    background-color: #ffeeee;
    border-left: 4px solid #FF0000;
    color: #000;
}}

#chapter-list li.pass:hover {{
    background-color: #eeffee;
    border-left: 4px solid #00AA00;
    color: #000;
}}

/* Default hover for unknown status */
#chapter-list li:not(.fail):not(.pass):hover {{
    background-color: #f4f4f4;
    color: #000;
}}
            #speed-control {{
                margin-left: 12px;
                font-size: 11px;
            }}
            #maximize-button {{
                font-size: 11px;
                padding: 5px 8px;
                border: none;
                background-color: #007bff;
                color: #fff;
                border-radius: 5px;
                cursor: pointer;
            }}

    #chapter-list {{
        background: #f4f4f4;
        padding: 8px;
        overflow-y: auto; /* Enable scrolling if chapters exceed the height */
        border-right: 1px solid #ddd;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    }}

    #chapter-list h3 {{
        text-align: center;
        margin-bottom: 10px;
        font-size: 14px;
        font-weight: bold;
        color: #333;
    }}

    #chapter-list ul {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}

    #chapter-list li {{
        margin-bottom: 8px;
        padding: 3.5px;
        cursor: pointer;
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 12px;
        transition: background 0.3s, color 0.3s;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis; /* Handle long titles */
    }}

    #chapter-list li:hover {{
        background: #007bff;
        color: #fff;
    }}

    /* Status styles for chapter list items */
    #chapter-list li.fail {{
        border-left: 4px solid #FF0000;
    }}

    #chapter-list li.pass {{
        border-left: 4px solid #00AA00;
    }}

    #maximize-button:hover {{
        background-color: #0056b3;
    }}

    #tooltip {{
        position: absolute;
        background-color: #333;
        color: #fff;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 11px;
        visibility: hidden;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
        transform: translate(-50%, -100%);
        white-space: nowrap;
    }}

    #tooltip.fail {{
        background-color: #AA0000;
    }}

    #tooltip.pass {{
        background-color: #007700;
    }}
#chapter-list li.selected {{
    background-color: #f0f6ff; /* Lighter, softer blue background */
    border-left: 4px solid #2196f3; /* Clean, professional border */
    transition: background-color 0.3s ease; /* Smooth transition */
     font-weight: bold;
                box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
                z-index: 10;
}}

#chapter-list li.selected:hover {{
    background-color: #e6f2ff; /* Subtle hover effect */
}}

#chapter-list li.selected.fail {{
                background-color: #ffdddd;
    color:black; /* Muted red text */
                border-left: 6px solid #FF0000;
}}

#chapter-list li.selected.pass {{
                background-color: #ddffdd;
    color:black; /* Muted green text */
                border-left: 6px solid #00AA00;
}}
        </style>
    </head>
    <body>
        <div id="chapter-list">
            <h3>Chapters</h3>
           <ul>
                {"".join([f'<li data-time="{start_time}" data-status="{step_status.get(title, "UNKNOWN").lower()}" class="{step_status.get(title, "UNKNOWN").lower()}">{title}</li>' for start_time, title in chapters])}
            </ul>
        </div>
        <div id="video-container">
             <video id="video" src="{os.path.basename(video_path)}" type="video/webm" preload="auto"></video>
            <div id="tooltip"></div>

            <div id="progress-bar-container">
                <div id="progress-bar"></div>
                {"".join([f'<div class="chapter-marker {step_status.get(title, "UNKNOWN").lower()}" style="left: {start_time / total_duration * 100}%" data-time="{start_time}" data-status="{step_status.get(title, "UNKNOWN").lower()}" title="{title}"></div>' for start_time, title in chapters])}
            </div>
            <div id="controls">
                <div id="controls-left">
                    <button id="play-button">Play</button>
                    <div id="time-display">00:00 / {format_time(total_duration)}</div>
                    <div id="current-step" class="step-status-unknown"></div>
                </div>
                <div id="controls-right">
                    <button id="maximize-button">Maximize</button>
                    <select id="speed-control">
                        <option value="1.0">1x</option>
                        <option value="1.5">1.5x</option>
                        <option value="2.0">2x</option>
                        <option value="0.5">0.5x</option>
                    </select>
                </div>
            </div>
        </div>

         <script>
        // Get the video file name from the path
const videoFileName = "{os.path.basename(video_path)}";

// Function to get the video path and handle both encoded and unencoded URLs
function getVideoPath() {{
    const currentPath = window.location.pathname;
    const directoryPath = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
    return directoryPath + videoFileName;
}}

document.addEventListener('DOMContentLoaded', function() {{
    const video = document.getElementById('video');
    // Set the video source
    video.src = getVideoPath();
    video.type = "video/webm";

    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBar = document.getElementById('progress-bar');
    const playButton = document.getElementById('play-button');
    const timeDisplay = document.getElementById('time-display');
    const currentStep = document.getElementById('current-step');
    const maximizeButton = document.getElementById('maximize-button');
    const speedControl = document.getElementById('speed-control');
    const videoContainer = document.getElementById('video-container');
    const chapterList = document.querySelectorAll('#chapter-list li');
    const tooltip = document.getElementById('tooltip');

    const chapters = {str(chapters_json)};
    const totalDuration = {total_duration};

    function clearSelectedChapters() {{
            chapterList.forEach(chapter => {{
                chapter.classList.remove('selected');
            }});
    }}

    // Flag to track if we need to autoplay after loading
    let shouldAutoplayOnLoad = false;
    let pendingSeekTime = null;

    // Check for step parameter immediately
    checkForStepInFullPath();

    // Special function to check if step parameter is in the full URL/path
    function checkForStepInFullPath() {{
        // Get the raw full URL
        const fullUrl = window.location.href;
        const lowerUrl = fullUrl.toLowerCase();

        // Look for pattern like "?step=step_2" or "?step=step2" anywhere in the URL
        const stepRegex = /[?&%]step=([^&]+)/i;
        const match = lowerUrl.match(stepRegex);

        if (match && match[1]) {{
            console.log("Found step in URL:", match[1]);
            shouldAutoplayOnLoad = true;
            prepareStepNavigation(decodeURIComponent(match[1]));
            return true;
        }}

        // Check for filename with embedded step parameter
        const pathParts = decodeURIComponent(fullUrl).split('/');
        const lastPart = pathParts[pathParts.length - 1];

        if (lastPart.includes('?step=')) {{
            const stepValue = lastPart.split('?step=')[1].split('&')[0];
            console.log("Found step in filename:", stepValue);
            shouldAutoplayOnLoad = true;
            prepareStepNavigation(stepValue);
            return true;
        }}

        return false;
    }}

    // Function to prepare step navigation (find the time but don't seek yet)
    function prepareStepNavigation(stepParam) {{
        if (!stepParam) return false;

        // Normalize step parameter by removing non-alphanumeric characters
        const normalizedParam = stepParam.toLowerCase().replace(/[^a-z0-9]/g, '');

        // Find matching chapter
        const requestedStep = chapters.find(chapter => {{
            const chapterTitle = chapter.title.toLowerCase().replace(/[^a-z0-9]/g, '');
            return chapterTitle.includes(normalizedParam) || normalizedParam.includes(chapterTitle);
        }});
        if (requestedStep) {{
            pendingSeekTime = requestedStep.start_time;
            return true;
        }}
        return false;
    }}

    // Function to actually handle step navigation
    function handleStepNavigation() {{
        if (pendingSeekTime !== null) {{
            video.currentTime = pendingSeekTime;
            pendingSeekTime = null;
            playVideo();
            return true;
        }}
        return false;
    }}

    // Function to safely play video with browser policy workaround
    function playVideo() {{
        const playPromise = video.play();

        if (playPromise !== undefined) {{
            playPromise
                .then(() => {{
                    // Video is playing
                    playButton.textContent = "Pause";
                    console.log("Video started playing successfully");
                }})
                .catch(error => {{
                    // Auto-play was prevented
                    console.log("Autoplay prevented:", error);
                    // We can show a UI element suggesting the user click play
                    playButton.classList.add('highlight-play-button');
                    setTimeout(() => {{
                        playButton.classList.remove('highlight-play-button');
                    }}, 2000);
                }});
        }}
    }}

    video.addEventListener('loadedmetadata', () => {{
        // Update time display immediately after metadata is loaded
        const currentTimeFormatted = formatTime(video.currentTime);
        const totalTimeFormatted = formatTime(video.duration);
        timeDisplay.textContent = `${{currentTimeFormatted}} / ${{totalTimeFormatted}}`;

        // Check if we need to autoplay at a specific position
        if (shouldAutoplayOnLoad) {{
            // Wait a moment to ensure the video is fully loaded
            setTimeout(() => {{
                handleStepNavigation();
            }}, 100);
        }}

        adjustVideoSize();
    }});

    // Also handle canplay event which might be more reliable for some browsers
    video.addEventListener('canplay', () => {{
        if (shouldAutoplayOnLoad && pendingSeekTime !== null) {{
            handleStepNavigation();
            shouldAutoplayOnLoad = false;
        }}
    }});

    function adjustVideoSize() {{
        const maxHeight = window.innerHeight - 120;
        video.style.maxHeight = maxHeight + "px";
        video.style.width = "100%";
    }}

    window.addEventListener('resize', adjustVideoSize);

    playButton.addEventListener('click', () => {{
        if (video.paused) {{
            playVideo();
        }} else {{
            video.pause();
            playButton.textContent = "Play";
        }}
    }});

  chapterList.forEach(chapter => {{
            chapter.addEventListener('click', () => {{
                const startTime = parseFloat(chapter.getAttribute('data-time'));

                // Remove 'selected' class from all chapters
                clearSelectedChapters();

                // Add 'selected' class to clicked chapter
                chapter.classList.add('selected');

                // Seek and play video
                video.currentTime = startTime;
                playVideo();
            }});
        }});

        // Update timeupdate event to highlight current chapter
        video.addEventListener('timeupdate', () => {{
            const progress = (video.currentTime / video.duration) * 100;
            progressBar.style.width = progress + '%';

            const currentTimeFormatted = formatTime(video.currentTime);
            const totalTimeFormatted = formatTime(video.duration);
        timeDisplay.textContent = `${{currentTimeFormatted}} / ${{totalTimeFormatted}}`;

            // Update current chapter display with status
            const currentChapterData = getCurrentChapterData(video.currentTime);
            if (currentChapterData) {{
                currentStep.textContent = currentChapterData.title;

                // Update the status class of the current step
                currentStep.className = ''; // Reset classes
            currentStep.classList.add(`step-status-${{currentChapterData.status.toLowerCase()}}`);

                // Highlight current chapter
                // Remove 'selected' from all chapters
                clearSelectedChapters();

                // Find and select the current chapter
                const currentChapterElement = Array.from(chapterList).find(
                    chapter => chapter.textContent === currentChapterData.title
                );

                if (currentChapterElement) {{
                    currentChapterElement.classList.add('selected');
                }}
            }} else {{
                currentStep.textContent = "";
                currentStep.className = '';
                currentStep.classList.add('step-status-unknown');

                // Remove 'selected' from all chapters when no chapter is current
                clearSelectedChapters();
            }}
        }});


    progressBarContainer.addEventListener('click', (e) => {{
        const clickX = e.offsetX;
        const newTime = (clickX / progressBarContainer.offsetWidth) * video.duration;
        video.currentTime = newTime;
    }});

    speedControl.addEventListener('change', () => {{
        video.playbackRate = parseFloat(speedControl.value);
    }});

    maximizeButton.addEventListener('click', () => {{
        if (video.requestFullscreen) {{
            video.requestFullscreen().then(() => {{
                adjustVideoSize();
            }});
        }}
    }});

    function formatTime(seconds) {{
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${{String(minutes).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;
    }}

    function getCurrentChapterData(currentTime) {{
        for (let i = 0; i < chapters.length; i++) {{
            if (currentTime >= chapters[i].start_time && (i === chapters.length - 1 || currentTime < chapters[i + 1].start_time)) {{
                return chapters[i];
            }}
        }}
        return null;
    }}

    // We need to modify this to return the title only
    function getCurrentChapter(currentTime) {{
        const chapterData = getCurrentChapterData(currentTime);
        return chapterData ? chapterData.title : "";
    }}

    // Handle click on tooltip - jump to that chapter
    tooltip.addEventListener('click', () => {{
        const chapterTitle = tooltip.textContent;
        const chapter = chapters.find(chap => chap.title === chapterTitle);

        if (chapter) {{
            video.currentTime = chapter.start_time;
        }}
    }});

    // Add click handlers to chapter markers
    document.querySelectorAll('.chapter-marker').forEach(marker => {{
        marker.addEventListener('click', () => {{
            const time = parseFloat(marker.getAttribute('data-time'));
            video.currentTime = time;
            playVideo();
        }});
    }});
}});
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    ...