import os

from PIL import Image
from rembg import remove


def remove_bg():
    if not os.path.isdir('images_without_bg'):
        os.mkdir('images_without_bg')
    for pict in os.listdir("input_imgs"):
        if pict.endswith('.png') or pict.endswith('.jpg') or pict.endswith('.jpeg') or pict.endswith('.JPG') \
                or pict.endswith('.JPEG') or pict.endswith('.PNG'):
            print(f'[+] Удаляю фон: "{pict}"...')
            output = remove(Image.open(os.path.join("input_imgs", pict)))
            output.save(os.path.join('images_without_bg', f'{pict.split(".")[0]}.png'))
        else:
            continue


def resize():
    if not os.path.isdir('images_resized'):
        os.mkdir('images_resized')
    for pict in os.listdir("images_without_bg"):
        original_image = Image.open(os.path.join("images_without_bg", pict)).convert("RGBA")
        width, height = original_image.size
        percentage = width/height
        print('[+] Исходный размер фото {wide} ширины x {height} '
              'высоты'.format(wide=width, height=height))

        if percentage >= 1:
            resized_image = original_image.resize((512, int(512/percentage)))
        else:
            resized_image = original_image.resize((int(512*percentage), 512))
        width, height = resized_image.size
        print('[+] Новый размер фото {wide} ширины x {height} '
              'высоты'.format(wide=width, height=height))
        datas = resized_image.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        resized_image.putdata(newData)
        resized_image.save(os.path.join('images_resized', f'{pict.split(".")[0]}.png'), "PNG")


if __name__ == '__main__':
    remove_bg()
    resize()