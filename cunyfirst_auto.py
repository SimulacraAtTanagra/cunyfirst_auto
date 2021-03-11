#new script for performing CF actions

from time import sleep
from seltools import mydriver,main
from cunydatatools import jsrename
from datetime import datetime,timedelta
from admin import colclean,newest
import pandas as pd
from selenium.webdriver.common.by import By
import time
from CF_PR_datapipeline import pr_data

class cunyfirst(main):
    loginurl="https://home.cunyfirst.cuny.edu/oam/Portal_Login1.html"
    unfield="CUNYfirstUsernameH"
    pwfield="CUNYfirstPassword"
    submit="submit"
    def login(self):    #consider moving this to seltools and usising data_dist
        self.driver.get(self.loginurl)
        self.waitfillid(self.unfield,self.un)
        self.waitfillid(self.pwfield,self.pw)
        self.main_window = self.driver.current_window_handle
        self.waitid(self.submit)
    def route(self):
        self.driver.switch_to.window(self.main_window)  
        self.waitlink(self.cfmodule)
        self.driver.switch_to.window(self.driver.window_handles[-1])
    def loginnow(self):
        self.login()
        self.route()
    def pagecheck(self):
        if self.driver.title == 'CUNY Login':
            self.login()
class hcm(cunyfirst):
    def __init__(self,driver,un=None,pw=None):
        self.driver=driver 
        if un:
            self.un=un
        else:
            self.un=input("Please enter your username.\n")
        if pw:
            self.pw=pw
        else:
            self.pw=input("Please enter your password.\n")
        
    cfmodule="Human Capital Management"
    
    def nav(self):
        for i in range(30):
            if self.driver.execute_script('return document.readyState;')!="complete":
                sleep(1)
                pass
            else:
                self.driver.get(self.url)
                sleep(1)
                if self.driver.execute_script('return document.readyState;')!="complete":
                    sleep(1)
                    pass
                else:
                    sleep(1)
                    if hasattr(self,'searchfield'):
                        self.switch_tar()
                        self.waitid(self.searchfield)
                    return(True)
    
    def swtich(self):
        self.waitid(self.navid)

    def move(self,num): #deprecate this once we have a dict way to navigate tabs
        self.waitid(self.links[num])
        self.wait_spin() 
    def createjob(self):
        return(hcm.jobpages(self,mydriver))
    def createpos(self):
        return(hcm.pospages(self))
    def createjs(self):
        return(hcm.jobsummary(self))
        
    def survey(self):
        pagelist=[]
        pagelist.append(self.driver.page_source)
        for i in range(6):
            try: 
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(i+1)
                pagelist.append(self.driver.page_source)
            except:
                pass
        return(pagelist)
    def survey2(self):
        pagelist=[]
        pagelist.append(self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))
        for i in range(6):
            try: 
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(i+1)
                pagelist.append(self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))
            except:
                pass
        return(pagelist)
    def proceed_check(self):
        while True:
            a=('visible' in [self.save_flag(self.save_check())])
            try:
                self.return_switch()
            except:
                self.okay2()
            b=self.spinner()
            try:
                self.return_switch()
            except:
                self.okay2()
            c=self.windowswitch("ICOK",0)
            try:
                self.return_switch()
            except:
                self.okay2()
            d=self.windowswitch("ALERTOK",0)
            if a==False and b==False and c==False and d==False:
                return(True)
                break
            else:
                print('waiting to complete last action')
                print([i[0] for i in [(name,value) for  name, value in locals().items()] if i[1]!=False])
                self.wait_spin()
                self.okay2()
                
    def close_pop(self):
        if len(self.driver.window_handles)>2:
            self.driver.switch_to.window(driver.window_handles[-1])
            self.cf_okay()
            self.driver.switch_to.window(driver.window_handles[-1])
            self.switch_tar()
            if "Log in with" in self.driver.page_source:
                self.login()
    
class cjr(hcm,main):
    def __init__(self,driver):
        self.driver=driver
        self.url='https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd_1/EMPLOYEE/HRMS/c/CU_HCM.CU_R1013.GBL'
    def run_current(self,datadict=None):
        #TODO add instructions for running a CJR to a specified folder(?)
        self.cf_okay(1)
        self.switch_tar()   #what we want is in the Target Content frame
        self.waitid("#ICSearch")    #if you've only saved one of this search..
        self.cf_okay(1) #waiting because it will take you to search params
        #filling out search params
        #for best results, we are doing as of today, always, Full Report
        #all fields other than Business Unit blank
        #if you've run this before, it shuld still have the prior details
        if datadict:
            datadict=datadict
        else:
            datadict={'CU_R1013_RUNCNT_ASOFDATE': datetime.now().strftime('%m/%d/%Y'),
             'CU_R1013_COMPAN_COMPANY$0': '',
             'CU_R1013_DEPT_DEPTID$0': '',
             'CU_R1013_BU_BUSINESS_UNIT$0': 'YRK01',
             'CU_R1013_EMPCLA_EMPL_CLASS$0': '',
             'CU_R1013_JOBCD_JOBCODE$0': '',
             'CU_R1013_EEO_EEO_JOB_GROUP$0': '',
             'CU_R1013_JOBFCT_JOB_FUNCTION$0': '',
             'CU_R1013_RUNCNT_FULL_PART_TIME': '',
             'CU_R1013_RUNCNT_HR_STATUS': '',
             'CU_R1013_PAYSTS_EMPL_STATUS$0': ''
                    }
        self.data_distribute(datadict)
        


class jobpages(hcm,main):
    def __init__(self, driver):
        self.driver=driver
        self.url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL"
        self.searchfield="EMPLMT_SRCH_COR_EMPLID"
    
    field1="EMPLMT_SRCH_COR_EMPLID"
    field2="EMPLMT_SRCH_COR_EMPL_RCD"
    search="#ICSearch"
    navid="ICTAB_1"
    save="#ICSave"
    tabs=["ICTAB_0","ICTAB_1","ICTAB_2","ICTAB_3","ICTAB_4","ICTAB_5"]
    links=["DERIVED_HR_JOB_DATA_BTN1","DERIVED_HR_JOB_DATA_BTN2","DERIVED_HR_JOB_DATA_BTN3","DERIVED_HR_JOB_DATA_BTN4","DERIVED_CU_JOB_DATA_BTN"]
    
    def add_row(self):
        self.switch_tar()
        self.waitid('$ICField12$new$0$$0')
        
    def swbdict(empldict,datething,seq):
            if empldict['JOB_EFFDT$0']==datething:
                seq=str(int(seq)+1)
            else:
                seq="0"
            empldict2={**empldict,**{"JOB_EFFSEQ$0":seq}}
            empldict2['JOB_ACTION$0']='Return From Work Break'
            empldict2["JOB_ACTION_REASON$0"]='Return From Work Break'
            seq=str(int(seq)+1)
            empldict={**empldict,**{"JOB_EFFSEQ$0":seq}}
            return(empldict,empldict2)
    def return_from(self,empldict):
        self.add_row()
        self.cf_data_distribute(empldict)
        self.cf_save[0]
    def return_switch(self):
        try:
            self.driver.switch_to.frame('TargetContent')
        except:
            self.driver.switch_to.default_content()
    
    def reappointment(self,dt=None,ation=None,reason=None,appthrs=None,prohrs=None):
        if dt:
            print("do soething here shane")
    def deletion_new(self):
        #step 1 - go into correction mode
        self.switch_tar()
        self.waitid("#ICCorrection")
        self.cf_save(1) #deprecated wait_spin for cf_save(1)
        #step 2 - remove position number
        self.switch_tar()
        y=self.getvals("JOB_POSITION_NBR$0")
        if len(y)>2:
            self.data_distribute({"JOB_POSITION_NBR$0":''})
        self.cf_save(0)
        #step 3 - remove end date
        self.switch_tar()
        z=self.getvals("JOB_EXPECTED_END_DATE$0")
        if len(z)>2:
            self.data_distribute({"JOB_EXPECTED_END_DATE$0":''})
            self.cf_save(0)
        #step 4 - change effective date
        self.switch_tar()
        x=self.getvals("JOB_EFFDT$0")
        #changing the effective date to yesterday should work in most cases.
        x=(datetime.strptime(x, "%m/%d/%Y")-timedelta(days=1)).strftime("%m/%d/%Y")
        self.data_distribute({"JOB_EFFDT$0":x})
        self.cf_save(1)
        self.cf_save(0)
        #step 5 - time to change action and reason
        self.switch_tar()
        x=self.dropdownitembyid("JOB_ACTION$0")
        y=self.dropdownitembyid("JOB_ACTION$0")
        if x!="Data Change":
            term="Data Change"
        else:
            term="Reappointment"
        while x==y:
            self.data_distribute({"JOB_ACTION$0":term})
            y=self.dropdownitembyid("JOB_ACTION$0")
            self.cf_save(1)
        termdict={"Data Change":"Revision","Reappointment":"Reappointment"}
        term=termdict[term]
        #step -6 changing reason
        self.cf_save(1) #wait_spin
        self.switch_tar()
        x=self.dropdownitembyid("JOB_ACTION_REASON$0")
        y=self.dropdownitembyid("JOB_ACTION_REASON$0")
        while y==x:
            self.data_distribute({"JOB_ACTION_REASON$0":term})
            y=self.dropdownitembyid("JOB_ACTION_REASON$0")
            self.cf_save(1)
        #changing to Data Change/ Revision ALWAYS returns end date, thus remove
        self.switch_tar()
        z=self.getvals("JOB_EXPECTED_END_DATE$0")
        if len(z)>2:
            self.data_distribute({"JOB_EXPECTED_END_DATE$0":''})
            self.cf_save(0)
        #finally, remove record.
        self.switch_tar()
        self.waitid("$ICField12$delete$0$$0")
        self.cf_save(1)
        self.cf_save(0)

    def open_this(self,empldict):
        self.data_distribute(empldict)
        self.waitid(self.search)
        self.wait_spin()
        try:
            self.driver.find_element_by_id("SEARCH_RESULT1").click()
            self.wait_spin()
        except:
            pass
    def massdeletion(self,obj):
        if type(obj)!=list:
            for i in obj.code.values:
                sleep(1)
                self.open_record('job',[i[:-1],i[-1:]])
                self.wait_spin()
                if self.gettext("JOB_EMPL_STATUS$0")=="Terminated":
                    self.deletion()
                self.nav() 
        else:
            for i in obj:
                sleep(1)
                self.openrecord('job',[x for x in i])
                self.wait_spin()
                if self.gettext("JOB_EMPL_STATUS$0")=='Terminated':
                    self.deletion()
                self.nav()
    def revision(self,empldict):
        #TODO speed datadistribute by using page-specific data
        #TODO make visiting all pages mandatory if ther eis data from them
        empldict1=[v for k,v in empldict.items() if k in ["EMPLMT_SRCH_COR_EMPLID","EMPLMT_SRCH_COR_EMPL_RCD"]]
        empldict1=[str(max([int(x) for x in empldict1])),str(min([int(x) for x in empldict1]))]
        self.openrecord('job',empldict1)
        if self.getvals("JOB_EFFDT$0")==empldict["JOB_EFFDT$0"] and self.gettext("JOB_ACTION_DT$0")==datetime.now().strftime('%m/%d/%Y'):
            #unfortunately, this will prevent us from loading anything same dated
            #TODO fix this part of the function. Does require sequence validation.
            self.nav()
            return()
        elif datetime.strptime(self.getvals("JOB_EFFDT$0"),'%m/%d/%Y')>datetime.strptime(empldict["JOB_EFFDT$0"],'%m/%d/%Y'):
            self.nav()
            return()
        if self.gettext('JOB_EMPL_STATUS$0') == "Short Work Break":
            ding=self.getvals("JOB_EFFDT$0")
            dong=self.getvals("JOB_EFFSEQ$0")
            empldict,empldict2=self.swbdict(empldict,ding,dong)
            self.return_from(empldict2)
        self.add_row()
        #source=self.driver.page_source
        self.data_distribute(empldict)
        self.cf_save(1)
        try:
            self.cf_save(1)
            self.switch_tar()
            self.waitid("DERIVED_CU_JOB_DATA_BTN")
        except:
            self.cf_save(1)
            sleep(1)
            self.waitid("DERIVED_CU_JOB_DATA_BTN")
            sleep(1)
        self.data_distribute(empldict)
        self.cf_save(0)
        sleep(1)
        self.nav()
        
    def random_click(self):     #doesn't fucking work.
        self.driver.execute_script('el = document.elementFromPoint(440, 120); el.click();')
    class workloc:
        effdt="JOB_EFFDT$0"
        seq="JOB_EFFSEQ$0"
        hrstatus="JOB_HR_STATUS$0"
        prstatus="JOB_EMPL_STATUS$0"
        action="JOB_ACTION$0"
        reason="JOB_ACTION_REASON$0"
        expend="JOB_EXPECTED_END_DATE$0"
        position="JOB_POSITION_NBR$0"
        date_created="JOB_ACTION_DT$0"
        indicator="JOB_JOB_INDICATOR$0"
        add_row="$ICField12$new$0$$0"
        del_row="$ICField12$delete$0$$0"
        include_hist="#ICUpdateAll"
        correct_hist="#ICCorrection"
        find_row="$ICField12$hfind$0"
        notes="DERIVED_HR_NP_HR_NP_INVOKE_ICN$0"
    class notes:
        add_note="DERIVED_HR_NP_HR_NP_ADD_PB"
        note_type="HR_NP_NOTE_CU_NOTE_TYPE$0"
        subject="HR_NP_NOTE_HR_NP_SUBJECT$0"
        text="HR_NP_NOTE_HR_NP_NOTE_TEXT$0"
        save="DERIVED_HR_NP_HR_NP_SAVE_PB"
        
        
        
    class jobinfo:
        empl_class="JOB_EMPL_CLASS$0"
        officer="JOB_OFFICER_CD$0"
        reports_to="JOB_REPORTS_TO$0"
        jobcode="JOB_JOBCODE$0"
        fte_actual="JOB_ADDS_TO_FTE_ACTUAL$0"
        ft_status="JOB_FULL_PART_TIME$0"
        reg_temp="JOB_REG_TEMP$0"
    class joblabor:
        barg_unit="JOB_BARG_UNIT$0"
        labor_arg="JOB_LABOR_AGREEMENT$0"
        union_dt="JOB_ENTRY_DATE$0"
        union_fee="JOB_PAY_UNION_FEE$0"
        union_seniority="JOB_UNION_SENIORITY_DT$0"
        empl_category="JOB_EMPL_CTG$0"
        union_code="JOB_UNION_CD$0"
        recalc_seniority="DERIVED_HR_LBR_HR_SNR_DT_DEF_BTN$0"
    class payroll:
        pay_system="JOB_PAY_SYSTEM_FLG$0"
        paygroup="JOB_PAYGROUP$0"
        holiday="JOB_HOLIDAY_SCHEDULE$0"
        fica_status="JOB_FICA_STATUS_EE$0"
    class salary_plan:
        plan="JOB_SAL_ADMIN_PLAN$0"
        refresh_plan="DERIVED_HR_REFRESH_BTN$0"
        grade="JOB_GRADE$0" 
        grade_refresh="DERIVED_HR_REFRESH_BTN$12$$0"
        step="JOB_STEP$0"
        grade_entry_dt="JOB_GRADE_ENTRY_DT$0"
        step_entry_dt="JOB_STEP_ENTRY_DT$0"
    class compensation:
        comp_rt_fd="JOB_COMPRATE$0"
        comp_freq="JOB_COMP_FREQUENCY$0"
        default_pay="DERIVED_HR_CMP_DFLT_COMP_BTN$0"
        rate_code="COMPENSATION_COMP_RATECD$0"
        comp_rate="COMPENSATION_COMPRATE$0"
        calc_comp="DERIVED_HR_CMP_CALC_COMP_BTN$0"
    class cunyinfo:
        appt_hrs="CU_JOB_JR_CU_APPOINT_HRS$0"
        pro_hrs="CU_JOB_JR_CU_PROF_HRS$0"
        pay_percent="CU_JOB_JR_CU_LEAVE_PER_PAY$0"
    class emp_data:
        override_orig_dt="PER_ORG_INST_ORIG_HIRE_OVR$0"
        orig_dt="PER_ORG_INST_ORIG_HIRE_DT$0"
            
    
class pospages(hcm,main):
    def __init__(self, driver):
        self.driver=driver
        self.url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/MANAGE_POSITIONS.POSITION_DATA.GBL"    
        self.searchfield="POSITION_SRCH_POSITION_NBR"
        self.nav()
    """    
    def nav(self):
        self.outer_instance.nav(self.url,self.searchfield)
    def move(self,num):
        self.outer_instance.move(num)
    """
        
    field1="POSITION_SRCH_POSITION_NBR"
    search="#ICSearch"
    add_row="$ICField3$new$0$$0"
    save="#ICSave"
    
    def return_switch(self):
        try:
            self.driver.switch_to.frame('TargetContent')
        except:
            self.driver.switch_to.default_content()
            
    def update_pos(self,corr=None,activate=None,dt=None,newrt=None,dept=None,title=None,line=None,payserv=None,reason=None):
        if corr:
            if self.windowswitch("#ICCorrection",0):    
                self.waitid("#ICCorrection")
                self.wait_spin()
        else:
            if self.windowswitch(self.add_row,0):
                self.waitid(self.add_row)
                self.wait_spin()
                sleep(1)
        if dept:
            if self.windowswitch('POSITION_DATA_DEPTID$0',0):
                print('udpating department')
                try:
                    self.waitfillid('POSITION_DATA_DEPTID$0',dept)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_DEPTID$0',dept)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if newrt:
            if self.windowswitch('POSITION_DATA_REPORTS_TO$0',0):
                print('udpating reports to')
                try:
                    self.waitfillid('POSITION_DATA_REPORTS_TO$0',newrt)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_REPORTS_TO$0',newrt)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if dt:
            if self.windowswitch('POSITION_DATA_EFFDT$0',0):
                print('udpating date')
                try:
                    self.waitfillid('POSITION_DATA_EFFDT$0',dt)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_EFFDT$0',dt)
                self.wait_spin()
                self.okay2()
                self.return_switch()
            else:
                print('udpating date')
                self.return_switch()
                self.waitfillid('POSITION_DATA_EFFDT$0',dt)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if reason:
            if self.windowswitch('POSITION_DATA_ACTION_REASON$0',0):
                print('udpating updating reason')
                try:
                    self.waitfillid('POSITION_DATA_ACTION_REASON$0',reason)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_ACTION_REASON$0',reason)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if activate:
            if self.windowswitch("POSITION_DATA_EFF_STATUS$0",0):
                if self.dropdownitembyid("POSITION_DATA_EFF_STATUS$0")!='Active':
                    print('udpating Effective Status')
                    try:
                        self.dropdownselector("POSITION_DATA_EFF_STATUS$0",'Active')
                    except:
                        self.return_switch()
                        self.dropdownselector("POSITION_DATA_EFF_STATUS$0",'Active')
                    self.wait_spin()
            if self.windowswitch("POSITION_DATA_POSN_STATUS$0",0):
                print('udpating position status')
                if self.dropdownitembyid("POSITION_DATA_POSN_STATUS$0")!='Approved':
                    try:
                        self.dropdownselector("POSITION_DATA_POSN_STATUS$0",'Approved')
                    except:
                        self.return_switch()
                        self.dropdownselector("POSITION_DATA_POSN_STATUS$0",'Approved')
                    self.wait_spin()
        if self.windowswitch("ICTAB_1",0):
            print('switching tabs')
            self.waitid("ICTAB_1")
            sleep(1)
        if self.windowswitch("POSITION_DATA_UPDATE_INCUMBENTS$0",0):
            print('udpating incumbent checkbox')
            try:
                self.waitid("POSITION_DATA_UPDATE_INCUMBENTS$0")
            except:
                self.return_switch()
                self.waitid("POSITION_DATA_UPDATE_INCUMBENTS$0")
            self.okay2()
        sleep(1)
        self.simplesave()
        self.okay2()
    def mass_rt_upd(self,poslist,effdt,posnum):
        successlist=[]
        faillist=[]
        for i in poslist:   #gotta gather position numbers from CF to create poslist
            self.nav()
            try:
                self.openrecord("pos",[i])
                self.update_pos(newrt=posnum,dt=effdt,reason='RTC')
                successlist.append(i)
            except:
                faillist.append(i)
                pass
        print('Successes:')
        print(','.join(successlist))
        print('Failures')
        print(','.join(faillist))

class jobsummary(hcm,main):
    search=("#ICSearch")
    def __init__(self,driver):
        self.driver=driver
        self.url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/CU_E065_JOB_SUMMARY.CU_JOB_SUMMARY.GBL"
        self.searchfield="CU_JOB_SUM_SRCH_EMPLID"
    def survey(self):
        return(self.outer_instance.survey())
    def nav(self):
        self.outer_instance.nav(self.url,self.searchfield)
    def downloader(self,emplid):
        self.data_distribute({"CU_JOB_SUM_SRCH_EMPLID":f'{emplid}'})
        self.waitid(self.search)
        self.wait_spin()
        self.waitid("ICTAB_HIDE_29")
        sleep(1)
        self.waitid("WF_JOB_SUMM$hexcel$0")
        sleep(5)
        jsrename(emplid,download_dir)
        self.nav()

class reports(object):
    
    def __init__(self, outer_instance):
        self.outer_instance = outer_instance
        self.driver=self.outer_instance.driver
    def run(self,searchbt,dt):
        self.waitid(searchbt)
        #if link, click link
        #insert dt in effective date field if exists
        #press run
        #press ok
        #wait preset period of time (or switch to another task)
        #press report manageer
        #waitspin
        #look for table containing report name "CURRENT DATA EXTRACT REPORT"
        #if found, click "CU_R1013"
        #waitid("URL$1")  IF the href ends in the filetype we're looking for, not "log"
    class cjr(object):
        url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/CU_HCM.CU_R1013.GBL"
            
def createdict(process_item):
    if type(process_item)=='list':
        empldict={}    
        empldict["EMPLMT_SRCH_COR_EMPLID"]=process_item[2]
        empldict["EMPLMT_SRCH_COR_EMPL_RCD"]=process_item[5]
        empldict["JOB_EFFDT$0"]=process_item[0]
        empldict['JOB_ACTION$0']='Data Change'
        empldict["JOB_ACTION_REASON$0"]="Revision"
        empldict["JOB_EXPECTED_END_DATE$0"]=process_item[6]
        empldict["CU_JOB_JR_CU_APPOINT_HRS$0"]=process_item[7]
    else:
        objlist=["EMPLMT_SRCH_COR_EMPLID","EMPLMT_SRCH_COR_EMPL_RCD","JOB_EFFDT$0",
                 'JOB_ACTION$0',"JOB_ACTION_REASON$0","JOB_EXPECTED_END_DATE$0",
                 "CU_JOB_JR_CU_APPOINT_HRS$0"]
        empldict={obj:process_item[obj] for obj in objlist}
    return(empldict)   

def parse_hr_trans(df):
    df=df[(df.Action=="Termination")&(df['Action Reason']=='Mass System Termination')]    
    df['code']= df['Employee ID'].astype('str')+df['Empl RCD'].astype('str')
    return(df[['code']])

def parsehtml(x):
    #use this on pagesource to turn html into a list of strings
    #makes it easy to scan portions of long html for particular substrings
    #also allows looking at surrounding code of that instance using index position
    x=x.replace(">","999999")
    x=x.replace("<","999999")
    x=x.replace(">","999999")
    x=x.split("999999")
    return(x)
    
def frame_search(driver,path):
    framedict = {}
    for child_frame in driver.find_elements_by_tag_name('frame'):
        child_frame_name = child_frame.get_attribute('name')
        framedict[child_frame_name] = {'framepath' : path, 'children' : {}}
        xpath = '//frame[@name="{}"]'.format(child_frame_name)
        driver.switch_to.frame(driver.find_element_by_xpath(xpath))
        framedict[child_frame_name]['children'] = frame_search(framedict[child_frame_name]['framepath']+[child_frame_name])
        #do something involving this child_frame
        driver.switch_to.default_content()
        if len(framedict[child_frame_name]['framepath'])>0:
            for parent in framedict[child_frame_name]['framepath']:
                parent_xpath = '//frame[@name="{}"]'.format(parent)
                driver.switch_to.frame(driver.find_element_by_xpath(parent_xpath))
    return framedict

def find_all_iframes(driver):
    #TODO Improve this code. Still fails in CJR module in CF
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    print(len(iframes))
    for index, iframe in enumerate(iframes):
        print(iframe.text)
        driver.switch_to.frame(index)
        find_all_iframes(driver)
        driver.switch_to.parent_frame()

#TODO function that closes open popup using driver.window_handles and counting
if __name__ == "__main__":
    download_dir="C:\\Users\\shane\\downloads"
    driver=mydriver.setupbrowser(mydriver(download_dir))
    home=hcm(driver,un=USERNAME,pw=PASSWORD)
    home.loginnow()
    #job=jobpages(home.driver)
    #job.nav()
    cjr=cjr(home.driver)
    cjr.nav()
    """while True:
        cjr.close_pop()
    filefolder=""
    listoftups=pr_data(filefolder,flag=True)
    listofdicts=pr_data(filefolder)
    
    for ix,i in enumerate(listoftups):
        try:
            job.nav()
            job.openrecord("job",i)
            job.deletion_new()
            print(f'record {ix} complete.')
        except:
            print(f'problem with record {ix}')
            job.nav()
    
    for ix,i in enumerate(listofdicts):
        start_time = time.time()
        try:
            job.revision(i)
            print(f'completing item {ix}.')    
        except:
            print(f'error with item {ix}')
            job.nav()
        print("Currently at : %s seconds using given test case" % (time.time() - start_time))
    """