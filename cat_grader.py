from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.clock import Clock
from playsound import playsound
from kivy.uix.screenmanager import ScreenManager, Screen
import cat_logic


# Add Backgrounds to label/caption 
# Change look of the buttons
# Delete db button
# show cat from your collection button
# configure sql to work on others computers and not need a password

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        Clock.schedule_once(self.load_image, 0)
        Clock.schedule_once(self.load_main, 0)
        # This BoxLayout just displays text
        self.caption = BoxLayout(orientation='vertical', size_hint=(1, .2))
        #self.add_widget(self.caption)
        self.l1 = Label(text="Rate your cat!", font_size=('40sp'), color=(0, 1, 0))
        #self.caption.add_widget(self.l1)

        # The GridLayout contains all the buttons for next cat and rating
        self.grid = GridLayout(cols=11, size_hint=(1, .3))
        
        # This layout is for buttons that delete the database and show cats from your collection
        self.database_layout = GridLayout(cols=2, size_hint=(1, .3))

        # Define Rating Buttons
        self.new_cat_button = Button(text="next cat", padding=43, size_hint=(1, 1), on_press=self.next_cat_pressed, background_color=[.4, .4, .4, .4])
        
        # Button to delete database as well as clear cat saved pics from folder
        self.drop_db_button = Button(text="Delete ratings & cats and exit", on_press=self.delete_db, background_color=[.4, .4, .4, .4])

        # Show top cats button
        self.show_top_cats = Button(text="Show top cats", background_color=[.4,.4,.4,.4], on_press=self.top_cats)

        
    def load_image(self, dt):
        # The Main area will be for images of cats
        self.image_data, self.content = cat_logic.call_api()
        self.cat_picture_data = self.image_data
        self.core_cat_image = CoreImage(self.cat_picture_data, ext='png')
        self.cat_picture = Image(texture=self.core_cat_image.texture, fit_mode="fill")       
        self.add_widget(self.cat_picture)
        
        
    def load_main(self, dt):
        self.add_widget(self.caption)
        self.caption.add_widget(self.l1)
        self.add_widget(self.grid)
        self.grid.add_widget(self.new_cat_button)
        # Loop for button creation that also adds them to the GridLayout at the bottom
        for i in range(10):
            i += 1
            b = Button(text=str(i), size_hint=(.5, 1), on_press=self.rating_pressed, background_color=[.4, .4, .4, .4])
            self.grid.add_widget(b)
        self.add_widget(self.database_layout)
        self.database_layout.add_widget(self.drop_db_button)
        self.database_layout.add_widget(self.show_top_cats)

    def delete_db(self, *instance):
        cat_logic.clear_database_table_and_images()
        App.get_running_app().stop()
    
    def rating_pressed(self, instance):
        playsound("sounds\\button.mp3")
        rating = instance.text
        cat_logic.generate_cat_image_file(self.content, rating)
        self.next_cat_pressed()

        

    def next_cat_pressed(self, *instance):
        playsound("sounds\\next_cat.mp3")
        self.image_data, self.content = cat_logic.call_api()
        self.cat_picture_data = self.image_data
        self.core_cat_image = CoreImage(self.cat_picture_data, ext='png') 
        self.cat_picture.texture = self.core_cat_image.texture

    def top_cats(self, *instance):
        random_top_cat = cat_logic.show_favorite_cats() 
        playsound("sounds\\next_cat.mp3")
        self.core_cat_image = CoreImage(random_top_cat, ext='png') 
        self.cat_picture.texture = self.core_cat_image.texture

class cat_grader(App):
    def build(self):
        return Main()

cat_grader().run()