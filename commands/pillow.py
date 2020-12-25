# -*- encoding:utf-8 -*-
import typing

from discord.ext import commands
from discord import File, Member, User
from PIL import Image, ImageDraw
import io
import colorgram

class Gen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pillow', description='')
    async def pillow(self, ctx, user: typing.Union[Member, User] = None):
        """
        Ceci est un commentaire
        """

        if not user:
            user = ctx.author

        IMAGE_WIDTH = 500
        IMAGE_HEIGHT = 700

        image = Image.new('RGB', size=(IMAGE_WIDTH, IMAGE_HEIGHT), color=(231, 76, 60))

        draw = ImageDraw.Draw(image)

        # gap = 30
        # draw.rectangle([gap, gap, IMAGE_WIDTH - gap, IMAGE_HEIGHT - gap], fill=(255, 255, 255))

        # --- avatar ---

        AVATAR_SIZE = 170

        # get URL to avatar
        # sometimes `size=` doesn't gives me image in expected size so later I use `resize()`
        avatar_asset = user.avatar_url_as(format='jpg')

        # read JPG from server to buffer (file-like object)
        buffer_avatar = io.BytesIO(await avatar_asset.read())

        #    buffer_avatar = io.BytesIO()
        #    await avatar_asset.save(buffer_avatar)
        #    buffer_avatar.seek(0)

        # read JPG from buffer to Image
        avatar_image = Image.open(buffer_avatar)


        # Palette
        colors_p_avatar = colorgram.extract(avatar_image, 6)

        # Circles

        color_circle = colors_p_avatar[0].rgb

        # size : 351
        draw.ellipse((-119, -78, (-119 + 351), (-78 + 351)), fill=color_circle)

        # size : 250
        draw.ellipse((375, -125, (375 + 250), (-125 + 250)), fill=color_circle)
        draw.ellipse((326, 217, (326 + 250), (217 + 250)), fill=color_circle)
        draw.ellipse((-82, 520, (-82 + 250), (520 + 250)), fill=color_circle)

        # size : 150
        draw.ellipse((73, 317, (73 + 150), (317 + 150)), fill=color_circle)
        draw.ellipse((267, 584, (267 + 150), (584 + 150)), fill=color_circle)

        # resize it
        avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))  #

        circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
        circle_draw = ImageDraw.Draw(circle_image)
        circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
        # avatar_image.putalpha(circle_image)
        # avatar_image.show()

        image.paste(avatar_image, (16, 16), circle_image)

        # create buffer
        buffer = io.BytesIO()

        # save PNG in buffer
        image.save(buffer, format='PNG')

        # move to beginning of buffer so `send()` it will read from beginning
        buffer.seek(0)

        await ctx.send(file=File(buffer, f'toto.png'))


def setup(bot):
    try:
        bot.add_cog(Gen(bot))
        bot.logger.info(f'$GREENLoaded $BLUE"pillow" $GREENcommand!')
    except Exception as e:
        bot.logger.error(f'$REDError while adding command $BLUE"pillow"', exc_info=e)
