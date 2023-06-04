from django.shortcuts import render,redirect
from .form import *
from moviepy.editor import *
from moviepy.video.fx.all import *
import os
import random
from zipfile import ZipFile
from os.path import basename
#from .videomerger import *
# Create your views here.

def index(request):
    if request.method == 'POST':
        o_videos = request.FILES.getlist('original_video')
        m_videos = request.FILES.getlist('merged_video')
        scale = request.POST.get('scale')
            #clip1 = VideoFileClip(i.path)
            #durationc1=clip1.duration
            #print(durationc1)
            #clip2 = VideoFileClip(two)
            #durationc2=clip2.duration
        """ video_form= VideoForm(request.POST, request.FILES)
        if video_form.is_valid():
            video_form.save()
            return redirect('templates') """

        O_Video.objects.all().delete()
        M_Video.objects.all().delete()
        Output_Video.objects.all().delete()

        for o_video in o_videos:
            o_vid = O_Video.objects.create(
                original_video=o_video,
            )
          
        for m_video in m_videos:
            m_vid = M_Video.objects.create(
                merged_video=m_video,
            )
                
        o_vid.save()
        m_vid.save()
        return redirect('preview')

    context = {}
    return render(request, 'merger_tools/index.html', context)


def cropp9_16(clip,n):
    (w, h) = clip.size
    try:
        if w>h:
            clip=clip.fx(vfx.resize,(h,h))
        (w,h)=clip.size

        if n=="top":
            left = 0
            top = 0
            right = w
            bottom = w
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

        elif n=="middle":
            clip = vfx.crop(clip, width=w, height=w, x_center=w/2, y_center=h/2)
        elif n=="bottom":
            left = 0
            top = h-w
            right = w
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

        elif n=='right':
            (w, h) = clip.size
            left = w/2
            top = 0
            right = w
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)
        elif n=='middle_side':
            (w, h) = clip.size
            left = w/4
            top = 0
            right = w-w/4
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

        elif n=='left':
            (w, h) = clip.size
            left = 0
            top = 0
            right = w/2
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

    except:
        pass

    return clip


def cropp1_1(clip,n):
    (w, h) = clip.size
    try:
        if w>h:
            clip=clip.fx(vfx.resize,(h,h))

        if n=="top":
            left = 0
            top = 0
            right = w
            bottom = w/2
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

        elif n=="middle":
            clip = vfx.crop(clip, width=w, height=w/2, x_center=w/2, y_center=h/2)
        elif n=="bottom":
            left = 0
            top = h-w/2
            right = w
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

        elif n=='right':
            (w, h) = clip.size
            if w<=h/2:
                return clip
            half=h/2
            left = w-half
            top = 0
            right = w
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

        elif n=='left':
            (w, h) = clip.size
            if w<=h/2:
                return clip
            half=h/2
            left = 0
            top = 0
            right = h/2
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)
        elif n=='middle_square':
            (w, h) = clip.size
            if w<=h/2:
                return clip
            half=h/2
            deduct=(w-half)/2
            left = deduct
            top = 0
            right = w-deduct
            bottom = h
            clip = vfx.crop(clip,x1=left, y1=top, x2=right, y2=bottom)

    except:
        pass
    return clip

def temp1(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)

            d1=clip1.duration
            d2=clip2.duration

            w1,h1=clip1.size
            w2,h2=clip2.size
            tobecut1 = h1-w1
            tobecut2 = h2-w2

            clip1=cropp9_16(clip1,crop_o)
            clip2=cropp9_16(clip2,crop_m)
                
            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip1],[clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip1],[clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip1],[clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            n+=1
    return n

def temp2(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path
            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)
            d1=clip1.duration
            d2=clip2.duration

            w1,h1=clip1.size
            w2,h2=clip2.size
            tobecut1 = h1-w1
            tobecut2 = h2-w2
            
            clip1=cropp9_16(clip1,crop_o)
            clip2=cropp9_16(clip2,crop_m)
            
            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip2],[clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip2],[clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip2],[clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)       

            n+=1


def temp3(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)
            
            d1=clip1.duration
            d2=clip2.duration
            
            clip1=cropp9_16(clip1,crop_o)
            clip2=cropp9_16(clip2,crop_m)

            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip1,clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
        
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip1,clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip1,clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            n+=1

def temp4(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)
            
            d1=clip1.duration
            d2=clip2.duration

            clip1=cropp9_16(clip1,crop_o)
            clip2=cropp9_16(clip2,crop_m)

            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip2,clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip2,clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip2,clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            n+=1

def temp5(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)

            d1=clip1.duration
            d2=clip2.duration
            clip1=cropp1_1(clip1,crop_o)
            clip2=cropp1_1(clip2,crop_m)

            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip1],[clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip1],[clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip1],[clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)

            n+=1


def temp6(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)
            
            d1=clip1.duration
            d2=clip2.duration
            clip1=cropp1_1(clip1,crop_o)
            clip2=cropp1_1(clip2,crop_m)

            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip2],[clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip2],[clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip2],[clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            n+=1


def temp7(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)
            
            d1=clip1.duration
            d2=clip2.duration
            clip1=cropp1_1(clip1,crop_o)
            clip2=cropp1_1(clip2,crop_m)
            
            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip1,clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip1,clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip1,clip2]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            n+=1

def temp8(sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0

    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path

            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)
            
            d1=clip1.duration
            d2=clip2.duration
            clip1=cropp1_1(clip1,crop_o)
            clip2=cropp1_1(clip2,crop_m)

            if d2 > d1:
                clip2 = clip2.subclip(0, d1)
                clips = [[clip2,clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)            
            elif d2 < d1:
                loop=d1/d2
                l=[clip2]
                for i in range(int(loop)):
                    l.append(clip2)
                clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                clips = [[clip2,clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                clips = [[clip2,clip1]]
                clips=clips_array(clips)
                select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            n+=1


def select_sound(sound,o,m,n,clips,formats,resize,temp_size):
    if sound == 'no_sound':
        final1 = clips.without_audio()
    elif sound == "s_from_original": 
        AudioClip=AudioFileClip(o)
        final1 = clips.set_audio(AudioClip)
    elif sound == "s_from_merged":
        AudioClip=AudioFileClip(m)
        final1 = clips.set_audio(AudioClip)
    else:
        final1 = clips

    if temp_size == '9:16':
        if resize == 'HD':
            try:
                final1=final1.fx(vfx.resize,(1080,1920))
            except:
                pass
        else:
            try:
                final1=final1.fx(vfx.resize,(2160,3840))
            except:
                pass
    else:
        if resize == 'HD':
            try:
                final1=final1.fx(vfx.resize,(1080,1080))
            except:
                pass
        else:
            try:
                final1=final1.fx(vfx.resize,(2160,2160))
            except:
                pass
    try:
        final1.write_videofile(os.path.abspath("static/assets/output_video/output"+str(n)+"."+formats), fps = 30, codec = 'mpeg4')
    except:
        pass
    oo=Output_Video.objects.create(output=os.path.abspath("static/assets/output_video/output"+str(n)+".mp4"))
    oo.save()


def create_template(o_place,m_place,sound,formats,crop_o,crop_m,resize,temp_size):
    cutted_o = O_Video.objects.all()
    cutted_m = M_Video.objects.all()
    n=0
    for i in cutted_o:
        o = i.original_video.path 
        for j in cutted_m:
            m = j.merged_video.path
            
            clip1 = VideoFileClip(o)
            clip2 = VideoFileClip(m)

            d1=clip1.duration
            d2=clip2.duration

            if temp_size == '9:16':
                if o_place=='left' or o_place=='right':
                    if crop_o=='middle' and crop_m=='middle':
                        crop_o='middle_square'
                        crop_m='middle_square'
                        clip1=cropp9_16(clip1,crop_o)
                        clip2=cropp9_16(clip2,crop_m)
                    elif crop_m=='middle':
                        crop_m='middle_square'
                        clip1=cropp9_16(clip1,crop_o)
                        clip2=cropp9_16(clip2,crop_m)
                    elif crop_o=='middle':
                        crop_o='middle_square'
                        clip1=cropp9_16(clip1,crop_o)
                        clip2=cropp9_16(clip2,crop_m)
                    else:
                        clip1=cropp9_16(clip1,crop_o)
                        clip2=cropp9_16(clip2,crop_m)
                else:
                    clip1=cropp9_16(clip1,crop_o)
                    clip2=cropp9_16(clip2,crop_m)
       
            elif temp_size == '1:1':
                if o_place=='left' or o_place=='right':
                    if crop_o=='middle' and crop_m=='middle':
                        crop_o='middle_square'
                        crop_m='middle_square'
                        clip1=cropp1_1(clip1,crop_o)
                        clip2=cropp1_1(clip2,crop_m)
                    elif crop_m=='middle':
                        crop_m='middle_square'
                        clip1=cropp1_1(clip1,crop_o)
                        clip2=cropp1_1(clip2,crop_m)
                    elif crop_o=='middle':
                        crop_o='middle_square'
                        clip1=cropp1_1(clip1,crop_o)
                        clip2=cropp1_1(clip2,crop_m)
                    else:
                        clip1=cropp1_1(clip1,crop_o)
                        clip2=cropp1_1(clip2,crop_m)
                else:
                    clip1=cropp1_1(clip1,crop_o)
                    clip2=cropp1_1(clip2,crop_m)


            if o_place=='top' and m_place=='bottom':
                if d2 > d1:
                    clip2 = clip2.subclip(0, d1)
                    clips = [[clip1],[clip2]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                elif d2 < d1:
                    loop=d1/d2
                    l=[clip2]
                    for i in range(int(loop)):
                        l.append(clip2)
                    clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                    clips = [[clip1],[clip2]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                else:
                    clips = [[clip1],[clip2]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)

            elif o_place=='bottom' and m_place=='top':
                if d2 > d1:
                    clip2 = clip2.subclip(0, d1)
                    clips = [[clip2],[clip1]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                elif d2 < d1:
                    loop=d1/d2
                    l=[clip2]
                    for i in range(int(loop)):
                        l.append(clip2)
                    clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                    clips = [[clip2],[clip1]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                else:
                    clips = [[clip2],[clip1]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)

            elif o_place=='left' and m_place=='right':
                if d2 > d1:
                    clip2 = clip2.subclip(0, d1)
                    clips = [[clip1,clip2]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                elif d2 < d1:
                    loop=d1/d2
                    l=[clip2]
                    for i in range(int(loop)):
                        l.append(clip2)
                    clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                    clips = [[clip1,clip2]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                else:
                    clips = [[clip1,clip2]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)

            elif o_place=='right' and m_place=='left':
                if d2 > d1:
                    clip2 = clip2.subclip(0, d1)
                    clips = [[clip2,clip1]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                elif d2 < d1:
                    loop=d1/d2
                    l=[clip2]
                    for i in range(int(loop)):
                        l.append(clip2)
                    clip2 =concatenate_videoclips(l).subclip(0, clip1.duration)
                    clips = [[clip2,clip1]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
                else:
                    clips = [[clip2,clip1]]
                    clips=clips_array(clips)
                    select_sound(sound,o,m,n,clips,formats,resize,temp_size)
            else:
                return 'The selected merging is not correct, please! select the right one'                

            n+=1


def preview(request):
    o_video = O_Video.objects.all()
    m_video = M_Video.objects.all()
    
    context={'o_video':o_video, 'm_video':m_video}
    return render(request, 'merger_tools/preview.html', context)


def templates(request):
    #video = O_Video.objects.all()
    error = ''
    if request.method == 'POST':
        Output_Video.objects.all().delete()

        temp_name1 = request.POST.get('temp1')
        temp_name2 = request.POST.get('temp2')
        temp_name3 = request.POST.get('temp3')
        temp_name4 = request.POST.get('temp4')
        temp_name5 = request.POST.get('temp5')
        temp_name6 = request.POST.get('temp6')
        temp_name7 = request.POST.get('temp7')
        temp_name8 = request.POST.get('temp8')

        formats = request.POST.get('format')
        
        crop_o = request.POST.get('crop_original')
        crop_m = request.POST.get('crop_merged')
        resize = request.POST.get('resize')
        temp_size = request.POST.get('temp-size')

        o_place = request.POST.get('o_place')
        m_place = request.POST.get('m_place')
        sound = request.POST.get('sound')
        
        if o_place!=None and m_place!=None and temp_size!=None:
            print(o_place,m_place,sound,formats,crop_o,crop_m,resize,temp_size)
            create_template(o_place,m_place,sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name1:
            temp_size = '9:16'
            temp1(sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name2: 
            temp_size = '9:16'
            temp2(sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name3:
            temp_size = '9:16'
            temp3(sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name4:
            temp_size = '9:16'
            temp4(sound,formats,crop_o,crop_m,resize,temp_size)  
        elif temp_name5:
            temp_size = '1:1'
            temp5(sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name6:
            temp_size = '1:1'
            temp6(sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name7:
            temp_size = '1:1'
            temp7(sound,formats,crop_o,crop_m,resize,temp_size)
        elif temp_name8:
            temp_size = '1:1'
            temp8(sound,formats,crop_o,crop_m,resize,temp_size) 
        else:
            print('Please select the correct template')
        return redirect('output')

    context = {'error':error}
    return render(request, 'merger_tools/template.html', context)

def output(request):
    outputs = Output_Video.objects.all()
    c=outputs.count()
    Zip_file.objects.all().delete()
    zip_name = 'allvideo.zip'
    with ZipFile(os.path.abspath('static/assets/download_zip/'+zip_name), 'w') as zipObj:
        for file in outputs:
                    filename=file.output.path
                    zipObj.write(filename, basename(filename))
    
    zipObj.close()

    if zip_name in os.path.abspath('static/assets/download_zip/'+zip_name):
        Zip_file.objects.create(file=zipObj.filename)
    zipf = Zip_file.objects.get()
    context = {'outputs':outputs,'zipf':zipf,'c':c}
    return render(request, 'merger_tools/output.html', context)
