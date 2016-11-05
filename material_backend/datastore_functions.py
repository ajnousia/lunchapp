import datetime
import model

def import_weekmenu_list_into_datastore(weeks_menu_list, restaurant_entity):
    for weeks_menu in weeks_menu_list:
        import_weekmenu_into_datastore(weeks_menu, restaurant_entity)

def import_weekmenu_into_datastore(weeks_menu, restaurant_entity):
    for dayMenu in weeks_menu:
        datastore_daymenu = model.DayMenu()
        datastore_daymenu_key = datastore_daymenu.put()
        datastore_daymenu_courses = []
        if len(dayMenu.courses) > 0:
            for course in dayMenu.courses:
                datastore_daymenu_course = model.Course(parent=datastore_daymenu_key)
                datastore_daymenu_course_key = datastore_daymenu_course.put()
                datastore_daymenu_course_components = []
                for component in course.components:
                    datastore_daymenu_course_component = model.Component(parent=datastore_daymenu_course_key)
                    datastore_daymenu_course_component.name = component.name
                    datastore_daymenu_course_component.properties = component.get_properties_as_string()
                    datastore_daymenu_course_component.date = dayMenu.date
                    datastore_daymenu_course_component.parent_restaurant = restaurant_entity.key
                    datastore_daymenu_course_components.append(datastore_daymenu_course_component)
                    datastore_daymenu_course_component.put()
                datastore_daymenu_course.components = datastore_daymenu_course_components
                datastore_daymenu_courses.append(datastore_daymenu_course)
                datastore_daymenu_course.parent_restaurant = restaurant_entity.key
                datastore_daymenu_course.date = dayMenu.date
                if course.price != None:
                    datastore_daymenu_course.price = float(course.price.replace(",", "."))
                datastore_daymenu_course.put()
        datastore_daymenu.courses = datastore_daymenu_courses
        datastore_daymenu.date = dayMenu.date
        datastore_daymenu.parent_restaurant = restaurant_entity.key
        datastore_daymenu.put()
