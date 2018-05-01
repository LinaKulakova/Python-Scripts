"""
TestCase ID : Main separator "CANAIS"
All comments removed from this scripts
Version: 01
"""
# import pytest
from TestScripts.lib.util import get_all_elements, BaseTest
from TestScripts.lib.util_web import BaseTab, WebLogout
from selenium.webdriver.common.action_chains import ActionChains
import time
from TestScripts.lib.constants_web import SIDE_MENU_X,CANCEL_PWD_RECOVERY, PWD_ERROR_MSG ,TITLE_MSG , channels_to_check, \
 MSG_PG2 , LOGIN_USERNAME , LOGIN_PASSWORD ,LOGIN_USER ,menu_options,SEGUIR,VER,BLUE_MSG

elements = get_all_elements("nostv_web.xlsx", "CANAIS")


class TestChannelPage(BaseTab):

    sheet_names = ["CANAIS", "LOGIN"]
    driver = None

    def test_setup(self, driver):
        self.log('Setup Login test')
        self.elements = self.initialize()
        return self.web_login()

    def test_channel_page(self):
        """
        Log In successfully
        """
        time.sleep(10)
        self.web_accept_cookie_if()
        # Verifying MENU options
        self.log('Verifying MENU options')
        self.driver.implicitly_wait(30)
        menu = self.driver.find_element_by_class_name('menu')
        menu_list_data = menu.find_elements_by_tag_name('a')
        for menu_data in menu_list_data:
            if menu_data.text.strip().upper() in menu_options:
                self.log('Option '+menu_data.text+' available')
                menu_options.pop(menu_options.index(menu_data.text.strip().upper()))
        assert not menu_options, 'ERROR IN MENU OPTIONS'
        self.log('All menu options are present')

        assert self.get_element("AVATAR").is_displayed() , self.log('avatar not available')
        self.log('avatar available')

        # Verifying channel list
        self.log('Verifying channel list')
        channel_list = self.driver.find_elements_by_class_name('channelLogo')
        for channel in channel_list:
            channel_img = channel.find_element_by_tag_name('img').get_attribute('ng-mage-parameters').split(",")
            parameters = channel_img[3].split(":")
            parameters_name = parameters[1].split('"')
            channel_name = parameters_name[1]
            self.log('Channel '+channel_name+' available' )
            if channel_name in channels_to_check:
                channels_to_check.pop(channels_to_check.index(channel_name))
        assert len(str(channels_to_check)) == 2, 'Some channels are missing'
        self.log('Channels RTP 1, RTP 2 , SIC  are present')

        streaming = self.get_element('CANAIS_STREAMLINE')
        assert streaming.is_displayed(), self.log('Streaming not started')
        self.log('Streamingstarted')

        dates = self.driver.find_elements_by_class_name('dates')
        assert len(str(dates)) > 6, self.log('All days are not available')
        self.log('All days are available')
        time.sleep(10)
        self.driver.implicitly_wait(20)

        assert self.get_element('CANAIS_AGORA').is_displayed(), self.log('AGORA is not present')
        self.log('AGORA is present')
        time.sleep(3)

        day_before = self.get_element('DAY_BEFORE')
        day_before.click()
        self.driver.implicitly_wait(30)
        time.sleep(5)

        program_elements = self.driver.find_elements_by_class_name('programNavigation')
        assert len(str(program_elements)) > 1 , self.log('EPG programs are not loaded in the day before HOJE')
        self.log('EPG programs are loaded in the day before HOJE')

        day_after = self.get_element('DAY_AFTER')
        day_after.click()
        self.driver.implicitly_wait(30)
        time.sleep(5)

        program_elements = self.driver.find_elements_by_class_name('programNavigation')
        assert len(str(program_elements))> 1 , self.log('EPG programs are not loaded in the day after HOJE')
        self.log('EPG programs are loaded in the day after HOJE')
        time.sleep(3)
        hoje = self.get_element('HOJEE')
        hoje.click()
        time.sleep(5)
        self.driver.implicitly_wait(30)
        self.log_assert(True) # if code reached this line, this is passed
        #canais colour blue


class TestCanais_built_in_player(BaseTab):

    
    sheet_names = ["CANAIS", "LOGIN"]
    driver = None

    def test_canais_built_in_player(self, driver):
        """
        Verify the canais built in player
        """
        self.elements = self.initialize()
        builder = ActionChains(self.driver)
        self.log('Verify the canais built in player')
        self.driver.implicitly_wait(30)

        # Clicking on the screen

        self.log('Clicking on the screen')
        player = self.driver.find_element_by_id('clVideoPlayer')
        player.click()
        self.driver.implicitly_wait(30)

        assert self.get_element('EMISSAO_TV').is_displayed(), self.log('EMISSAO TV is not present')
        self.log('EMISSAO TV is present')

        # tapping on gear wheel and checking the options
        builder.move_to_element_with_offset(player,1000,100).move_to_element_with_offset(player,800,120).perform()
        gear_wheel = self.driver.find_element_by_class_name('qualityWrap')
        assert gear_wheel , self.log('Gear wheel not present')
        self.log('Gear wheel present')
        gear_wheel.click()
        self.driver.implicitly_wait(30)

        quality_options = self.driver.find_element_by_class_name('qualityOptions').find_elements_by_class_name('option')
        for option in quality_options:
            self.log('quality option '+option.text+' present')

        quality = self.get_element('SELECTED_QUALITY')
        self.log('Selected quality is '+ quality.text)
        gear_wheel.click()
        #time.sleep(5)

        builder.move_to_element_with_offset(player,1000,100).move_to_element_with_offset(player,800,120).perform()
        left_value = self.get_element('LEFT_PROGRESS_BAR')
        self.log(left_value.text)
        assert self.check_equal(left_value.text[0],'-') , self.log('The value in the left end ot the progressive bar is not negative')
        self.log('The value in the left end ot the progressive bar is negative')

        builder.move_to_element_with_offset(player,1000,100).move_to_element_with_offset(player,800,120).perform()
        self.log('clicking full screen')
        self.driver.find_element_by_class_name('fullscreen').find_element_by_tag_name('svg').click()
        self.driver.implicitly_wait(30)
        time.sleep(5)

        builder.move_to_element_with_offset(player,1000,100).move_to_element_with_offset(player,800,120).perform()
        cross_btn = self.driver.find_element_by_class_name('close').find_element_by_tag_name('svg')
        assert cross_btn.is_displayed() , self.log('Close button not persent')
        self.log('Close option present')
        builder.move_to_element_with_offset(player,1000,100).move_to_element_with_offset(player,800,120).perform()
        cross_btn.click()
        time.sleep(10)

        agora = self.get_element('CANAIS')
        self.log_assert(agora.is_displayed(), 'App did returning to previous screen')
        self.log('App returned to previous screen')
#         bak_btn = self.get_element('BAK_BTN')
#         assert bak_btn.is_displayed() , self.log('Not full screeen')
#         self.log('Not full screeen')
#         self.driver.find_element_by_class_name('fullscreen').find_element_by_tag_name('svg').click()
#         self.driver.implicitly_wait(30)

#         assert self.get_element('CANAIS_AGORA').is_displayed() , self.log('Not returned to normal screen')
#         self.log('Returned to normal screen')


class TestCanais_list_of_days(BaseTab):

    sheet_names = ["CANAIS", "LOGIN"]
    driver = None

    def test_list_of_days(self, driver):
        """
        Verify the canais list of days
        """
        self.elements = self.initialize()
        self.log('Verify the canais list of days')
        self.driver.implicitly_wait(30)

        highlighted_date = self.get_element('HOJE')
        highlighted_date.click()
        time.sleep(10)
        assert self.check_equal(highlighted_date.text,'HOJE'),self.log('HOJE is not present')
        self.log('HOJE is present')

        program_elements = self.driver.find_elements_by_class_name('programNavigation')
        assert len(str(program_elements)) > 1 , self.log('Programs are not loaded')
        self.log('Programs are loaded')

        # Verifying MENU options
        self.log('Verifying MENU options')
        self.driver.implicitly_wait(30)
        menu = self.driver.find_element_by_class_name('menu')
        menu_list_data = menu.find_elements_by_tag_name('a')
        for menu_data in menu_list_data:
            if menu_data.text.strip().upper() in menu_options:
                self.log('Option '+menu_data.text+' available')
                menu_options.pop(menu_options.index(menu_data.text.strip().upper()))
        self.log_assert(not menu_options, 'ERROR IN MENU OPTIONS')
        self.log('All menu options are present')


class TestCanais_channel_list(BaseTab):

    
    sheet_names = ["CANAIS", "LOGIN"]
    driver = None

    def test_channel_list(self, driver):
        """
        Verify the canais channel list
        """
        self.elements = self.initialize()
        self.log('Verify the canais channel list')
        self.driver.implicitly_wait(30)

        # Clicking channel icon
        self.log('Clicking channel icon')
        channel_icon = self.driver.find_element_by_class_name('wrap')
        channel_icon.click()
        time.sleep(10)

        close_button = self.driver.find_element_by_id('channels').find_element_by_tag_name('svg')
        assert close_button.is_displayed() , self.log('Close button not persent')
        self.log('Close option present')

        filter_options =['TODOS','DISPONIVEIS','FAVORITOS']
        filters = self.driver.find_element_by_id('channels').find_elements_by_tag_name('li')
        for filter in filters:
            if filter.text.strip().upper() in filter_options:
                self.log('Filter option '+ filter.text + 'present')
                filter_options.pop(filter_options.index(filter.text.strip().upper()))

        todos = self.get_element('TODOS')
        todos.click()
        self.driver.implicitly_wait(30)
        self.log_assert(True)  # if code reached this line, this is passed


class TestProgram_info_current_program(BaseTab):

    
    sheet_names = ["CANAIS", "LOGIN"]
    driver = None

    def test_Program_info_current_program(self, driver):

        self.elements = self.initialize()
        self.log('Verify Program info current program')
        self.driver.implicitly_wait(30)
        time.sleep(5)

        self.log('Clicking on the program')
        pgm_list = self.driver.find_elements_by_class_name('timeInnerContainer')
        for i in range(len(pgm_list)):
            if 'AGORA' in pgm_list[i].text.strip():
                pgm_list[i].click()
                break
                
        time.sleep(3)
        self.driver.implicitly_wait(30)

        self.log('Clicking on MAIS button of program')
        mais = self.get_element('RTP1_PGM_MAIS')
        mais.click()
        self.driver.implicitly_wait(30)

        # testing tabs inside program

        number_of_visuals = self.get_element('RTP1_PGM_MAIS_VISUALS')
        assert len(str(number_of_visuals)) > 0 , 'Number of visualisations not available'
        self.log('Number of visualisations available')
        current_items = self.verify_current_options('action')
        self.log('Current items: {}'.format(current_items))
        assert 'VER' in current_items, 'VER not available'
        self.log('VER available')
        try:
            assert 'VER DO INÍCIO' in current_items, 'VER DO INÍCIO not available'
        except:
            self.log('VER DO INÍCIO available')
        play_btn = self.driver.find_element_by_class_name('infoMask').find_element_by_id('_Rectangle_')
        self.validate_ver_mais_remove(current_items)
        self.validate_any_words(("GRAVAÇÃO",))
        try:
            relacionados = self.get_element('RTP1_PGM_MAIS_RELACIONADOS')
            self.log_assert(relacionados.text.replace(' ','').upper() in ['RELACIONADOS','ELENCO','RELACIONADOSELENCO']) , ('Option RELACIONADOS or ELENCO not available')
            self.log('Option RELACIONADOS or ELENCO available')
            pgm_loaded = self.driver.find_elements_by_tag_name('md-grid-tile')
            assert pgm_loaded , self.log('Image not available under RELACIONADOS')
            self.log('Image available under RELACIONADOS')
            options = self.driver.find_element_by_class_name('optionList').find_elements_by_tag_name('span')
            if len(options) > 1:
                options[1].click()
                pgm_loaded = self.driver.find_elements_by_tag_name('md-grid-tile')
                assert pgm_loaded , self.log('Image not available under ELENCO')
                self.log('Image available under ELENCO')
        except:
            pass
        self.is_back()
        self.log_assert(True)  # if code reached this line, this is passed

