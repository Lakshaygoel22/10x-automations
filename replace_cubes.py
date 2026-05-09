import os
import re

new_cubes = """    <!-- Background 3D Cubes -->
    <div class="bg-cube-wrapper cube-1">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>
    <div class="bg-cube-wrapper cube-2">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>
    <div class="bg-cube-wrapper cube-3">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>
    <div class="bg-cube-wrapper cube-4">
        <div class="supply-box">
            <div class="box-face box-front"></div>
            <div class="box-face box-back"></div>
            <div class="box-face box-right"></div>
            <div class="box-face box-left"></div>
            <div class="box-face box-top"></div>
            <div class="box-face box-bottom"></div>
        </div>
    </div>

    <!-- Chat Widget -->"""

for f in os.listdir('static'):
    if f.endswith('.html'):
        with open(f"static/{f}", 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Regex to replace from Strong Corner Animation to Chat Widget
        content = re.sub(r'<!-- Strong Corner Animation -->.*?<!-- Chat Widget -->', new_cubes, content, flags=re.DOTALL)
        
        with open(f"static/{f}", 'w', encoding='utf-8') as file:
            file.write(content)
