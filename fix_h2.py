import re

def process_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Sizing classes to remove
    sizes = ['text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl', 'text-7xl', 'text-8xl', 'text-9xl']
    prefixes = ['', 'sm:', 'md:', 'lg:', 'xl:', '2xl:']
    to_remove = set([p + s for s in sizes for p in prefixes])
    to_remove.add('font-serif')
    to_remove.add('text-[#4A3E36]')
    to_remove.add('leading-tight')
    to_remove.add('leading-none')

    def fix_h2(match):
        tag = match.group(0)
        cls_match = re.search(r'class="([^"]+)"', tag)
        if cls_match:
            classes = cls_match.group(1).split()
            filtered = [c for c in classes if c not in to_remove]
            
            # The new ones to add
            new_classes = ['text-3xl', 'sm:text-4xl', 'lg:text-5xl', 'font-serif', 'text-[#4A3E36]', 'leading-tight']
            
            final_classes = new_classes + filtered
            
            # remove duplicates preserving order
            seen = set()
            deduped = []
            for c in final_classes:
                if c not in seen:
                    deduped.append(c)
                    seen.add(c)
                    
            return tag.replace(cls_match.group(0), f'class="{" ".join(deduped)}"')
        return tag

    new_content = re.sub(r'<h2[^>]*>', fix_h2, content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed h2 sizes")

process_file()
