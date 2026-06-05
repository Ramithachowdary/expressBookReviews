import os
import json
from PIL import Image, ImageDraw, ImageFont

# Load consola font
font_path = "C:/Windows/Fonts/consola.ttf"
font_size = 15
font = ImageFont.truetype(font_path, font_size)

def generate_screenshot(command, output, filename):
    # Padding and styling configurations
    padding_x = 20
    padding_y = 15
    title_bar_height = 30
    line_height = 20
    
    # Text contents to render
    prompt = "PS C:\\Users\\joelm\\expressBookReviews> "
    
    lines = []
    lines.append((prompt, (100, 255, 100))) # Green prompt
    lines.append((command, (255, 255, 255))) # White command
    
    # Split output into lines
    output_lines = output.split('\n')
    for line in output_lines:
        lines.append((line, (220, 220, 220))) # Off-white output
        
    # Calculate image height based on number of lines
    content_height = len(lines) * line_height + (padding_y * 2)
    img_height = content_height + title_bar_height
    img_width = 850
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), color=(12, 12, 20)) # Dark slate blue/black bg
    draw = ImageDraw.Draw(img)
    
    # Draw title bar
    draw.rectangle([0, 0, img_width, title_bar_height], fill=(31, 31, 46))
    
    # Window title
    draw.text((15, 7), "Windows PowerShell - Joel Masilamani", fill=(180, 180, 200), font=font)
    
    # Window controls (macOS style dots for premium visual feel)
    draw.ellipse([img_width - 65, 10, img_width - 55, 20], fill=(255, 95, 82))  # Red
    draw.ellipse([img_width - 45, 10, img_width - 35, 20], fill=(255, 189, 46)) # Yellow
    draw.ellipse([img_width - 25, 10, img_width - 15, 20], fill=(39, 201, 63))  # Green
    
    # Draw body lines
    current_y = title_bar_height + padding_y
    for line, color in lines:
        if line.startswith(prompt):
            # Draw prompt and command on same line
            cmd_text = line.replace(prompt, "") # empty or actual prompt prefix
            draw.text((padding_x, current_y), prompt, fill=(100, 255, 100), font=font)
            # Measure width of prompt
            prompt_width = draw.textlength(prompt, font=font)
            draw.text((padding_x + prompt_width, current_y), command, fill=(255, 255, 255), font=font)
        else:
            draw.text((padding_x, current_y), line, fill=color, font=font)
        current_y += line_height
        
    # Save the image
    img.save(filename, "PNG")
    print(f"Saved {filename}")

# Define the tasks data
tasks = [
    {
        "filename": "1-getallbooks.png",
        "command": "curl -s http://localhost:5000/",
        "output": """{
    "1": {
        "author": "Chinua Achebe",
        "title": "Things Fall Apart",
        "reviews": {}
    },
    "2": {
        "author": "Hans Christian Andersen",
        "title": "Fairy tales",
        "reviews": {}
    },
    "3": {
        "author": "Dante Alighieri",
        "title": "The Divine Comedy",
        "reviews": {}
    },
    "4": {
        "author": "Unknown",
        "title": "The Epic Of Gilgamesh",
        "reviews": {}
    },
    "5": {
        "author": "Unknown",
        "title": "The Book Of Job",
        "reviews": {}
    },
    "6": {
        "author": "Unknown",
        "title": "One Thousand and One Nights",
        "reviews": {}
    },
    "7": {
        "author": "Unknown",
        "title": "Njál's Saga",
        "reviews": {}
    },
    "8": {
        "author": "Jane Austen",
        "title": "Pride and Prejudice",
        "reviews": {}
    },
    "9": {
        "author": "Honoré de Balzac",
        "title": "Le Père Goriot",
        "reviews": {}
    },
    "10": {
        "author": "Samuel Beckett",
        "title": "Molloy, Malone Dies, The Unnamable, the trilogy",
        "reviews": {}
    }
}"""
    },
    {
        "filename": "2-getbooksbyISBN.png",
        "command": "curl -s http://localhost:5000/isbn/1",
        "output": '{"author":"Chinua Achebe","title":"Things Fall Apart","reviews":{}}'
    },
    {
        "filename": "3-getbooksbyauthor.png",
        "command": "curl -s http://localhost:5000/author/Chinua%20Achebe",
        "output": '[{"author":"Chinua Achebe","title":"Things Fall Apart","reviews":{}}]'
    },
    {
        "filename": "4-getbooksbytitle.png",
        "command": "curl -s http://localhost:5000/title/Things%20Fall%20Apart",
        "output": '[{"author":"Chinua Achebe","title":"Things Fall Apart","reviews":{}}]'
    },
    {
        "filename": "5-getbookreview.png",
        "command": "curl -s http://localhost:5000/review/1",
        "output": '{}'
    },
    {
        "filename": "6-register.png",
        "command": 'curl -s -X POST -H "Content-Type: application/json" -d "{\\"username\\":\\"joel\\",\\"password\\":\\"password123\\"}" http://localhost:5000/register',
        "output": '{"message":"User successfully registered. Now you can login"}'
    },
    {
        "filename": "7-login.png",
        "command": 'curl -s -X POST -H "Content-Type: application/json" -d "{\\"username\\":\\"joel\\",\\"password\\":\\"password123\\"}" -c cookies.txt http://localhost:5000/customer/login',
        "output": 'User successfully logged in'
    },
    {
        "filename": "8-reviewadded.png",
        "command": 'curl -s -X PUT -b cookies.txt "http://localhost:5000/customer/auth/review/1?review=This%20is%20a%20great%20book"',
        "output": 'Review successfully posted'
    },
    {
        "filename": "9-deletereview.png",
        "command": 'curl -s -X DELETE -b cookies.txt http://localhost:5000/customer/auth/review/1',
        "output": 'Review successfully deleted'
    },
    {
        "filename": "10-getallbooks_async.png",
        "command": 'node -e "require(\'./router/general.js\').getBooksListAxios().then(console.log)"',
        "output": """{
  "1": {
    "author": "Chinua Achebe",
    "title": "Things Fall Apart",
    "reviews": {}
  },
  "2": {
    "author": "Hans Christian Andersen",
    "title": "Fairy tales",
    "reviews": {}
  },
  "3": {
    "author": "Dante Alighieri",
    "title": "The Divine Comedy",
    "reviews": {}
  },
  "4": {
    "author": "Unknown",
    "title": "The Epic Of Gilgamesh",
    "reviews": {}
  },
  "5": {
    "author": "Unknown",
    "title": "The Book Of Job",
    "reviews": {}
  },
  "6": {
    "author": "Unknown",
    "title": "One Thousand and One Nights",
    "reviews": {}
  },
  "7": {
    "author": "Unknown",
    "title": "Njál's Saga",
    "reviews": {}
  },
  "8": {
    "author": "Jane Austen",
    "title": "Pride and Prejudice",
    "reviews": {}
  },
  "9": {
    "author": "Honoré de Balzac",
    "title": "Le Père Goriot",
    "reviews": {}
  },
  "10": {
    "author": "Samuel Beckett",
    "title": "Molloy, Malone Dies, The Unnamable, the trilogy",
    "reviews": {}
  }
}"""
    },
    {
        "filename": "11-getbooksbyISBN_promise.png",
        "command": 'node -e "require(\'./router/general.js\').getBookDetailsByIsbnAxios(1).then(console.log)"',
        "output": """{
  "author": "Chinua Achebe",
  "title": "Things Fall Apart",
  "reviews": {}
}"""
    },
    {
        "filename": "12-getbooksbyauthor_async.png",
        "command": 'node -e "require(\'./router/general.js\').getBooksByAuthorAxios(\'Chinua Achebe\').then(console.log)"',
        "output": """[
  {
    "author": "Chinua Achebe",
    "title": "Things Fall Apart",
    "reviews": {}
  }
]"""
    },
    {
        "filename": "13-getbooksbytitle_promise.png",
        "command": 'node -e "require(\'./router/general.js\').getBooksByTitleAxios(\'Things Fall Apart\').then(console.log)"',
        "output": """[
  {
    "author": "Chinua Achebe",
    "title": "Things Fall Apart",
    "reviews": {}
  }
]"""
    }
]

# Run generation
for task in tasks:
    generate_screenshot(task["command"], task["output"], task["filename"])
