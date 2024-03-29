from django import forms

from Configuration.countryConf import countries
from Configuration.stateConf import states
from General.models import CollegeYear, Semester, FacultySubject, Batch, Schedule, Branch, Schedulable, Division, Shift
from .models import Faculty, Subject, Student

# subject_list = []
# subject_list = Subject.objects.filter(is_active=True)

# faculty_list = []
# faculty_list = Faculty.objects.all()

# division_list = abcdef.objects.filter(is_active=True)
# division_list = []
# year_list = CollegeYear.objects.all()

# shift_list = []
# shift_list = Shift.objects.all()

gr_roll = '''student2	1
student	1
I1510432	3
test	322050
U1410306	322079
U1410625	321012
U1410613	321034
U1510016	321052
U1510019	321059
U1510028	321019
U1510040	321053
U1510042	321018
U1510061	321030
U1510080	321035
U1510091	321067
U1510093	321055
U1510114	321038
U1510121	321042
U1510125	321068
U1510135	321027
U1510139	321041
U1510145	321024
U1510174	321074
U1510187	321051
U1510191	321044
U1510194	321054
U1510199	321031
U1510230	321028
U1510238	321049
U1510257	321050
U1510265	321058
U1510278	321060
U1510290	321013
U1510298	321063
U1510305	321021
U1510309	321022
U1510312	321075
U1510315	321014
U1510325	321069
U1510331	321046
U1510334	321015
U1510335	321033
U1510340	321009
U1510347	321011
U1510359	321010
U1510375	321032
U1510379	321072
U1510406	321062
U1510414	321017
U1510416	321037
U1510445	321064
U1510446	321076
U1510471	321001
U1510472	321004
U1510479	321002
U1510480	321003
U1510485	321005
U1510491	321020
U1510496	321016
U1510497	321047
U1510524	321029
U1510533	321023
U1510536	321056
U1510556	321026
U1510569	321066
U1510575	321061
U1510584	321065
U1510624	321008
U1510644	321006
U1620011	321043
U1620033	321070
U1620037	321045
U1620050	321073
U1620075	321071
U1620088	321057
U1620092	321048
U1620116	321036
U1620184	321039
U1620201	321007
U1620212	321040
U1620214	321025
U1410337	322061
U1410438	322024
U1410538	322001
U1410556	322064
U1510002	322075
U1510007	322042
U1510033	322013
U1510053	322069
U1510058	322011
U1510071	322019
U1510085	322007
U1510101	322015
U1510105	322032
U1510122	322067
U1510127	322031
U1510136	322068
U1510141	322054
U1510148	322023
U1510151	322026
U1510153	322046
U1510161	322012
U1510184	322072
U1510201	322006
U1510208	322038
U1510215	322022
U1510233	322073
U1510254	322057
U1510266	322070
U1510281	322060
U1510292	322014
U1510299	322041
U1510300	322071
U1510323	322034
U1510344	322009
U1510367	322002
U1510371	322048
U1510374	322008
U1510378	322020
U1510380	322053
U1510383	322004
U1510398	322030
U1510431	322050
U1510448	322021
U1510452	322010
U1510464	322052
U1510470	322063
U1510478	322047
U1510483	322039
U1510487	322045
U1510506	322028
U1510520	322003
U1510521	322005
U1510522	322027
U1510525	322016
U1510565	322076
U1510579	322056
U1510590	322065
U1510607	322040
U1510620	322017
U1510621	322044
U1510623	322018
U1510638	322074
U1510639	322058
U1510641	322049
U1620051	322037
U1620053	322051
U1620054	322055
U1620056	322033
U1620064	322036
U1620069	322043
U1620109	322066
U1620122	322062
U1620138	322035
U1620147	322025
U1620160	322059
U1620194	322029
U1410119	323024
U1410499	323017
U1510001	323029
U1510008	323055
U1510013	323025
U1510015	323015
U1510032	323035
U1510038	323023
U1510046	323022
U1510063	323006
U1510069	323057
U1510074	323036
U1510089	323016
U1510092	323020
U1510103	323066
U1510118	323021
U1510126	323033
U1510131	323063
U1510134	323007
U1510137	323056
U1510154	323027
U1510156	323011
U1510163	323048
U1510166	323038
U1510172	323041
U1510188	323049
U1510234	323031
U1510244	323058
U1510245	323034
U1510256	323050
U1510268	323044
U1510270	323059
U1510297	323028
U1510301	323051
U1510313	323037
U1510319	323009
U1510332	323039
U1510333	323067
U1510337	323010
U1510377	323053
U1510386	323008
U1510403	323054
U1510436	323013
U1510490	323030
U1510501	323003
U1510510	323001
U1510511	323002
U1510512	323004
U1510529	323046
U1510530	323014
U1510534	323060
U1510578	323018
U1510589	323064
U1510619	323047
U1510651	323065
U1510653	323045
U1620014	323019
U1620022	323042
U1620035	323061
U1620089	323068
U1620139	323062
U1620144	323040
U1620150	323026
U1620154	323005
U1620181	323043
U1620197	323032
U1620206	323012
U1620233	323052
U1610005	221044
U1610007	221051
U1610011	221038
U1610012	221008
U1610014	221011
U1610016	221028
U1610032	221017
U1610033	221026
U1610043	221039
U1610065	221019
U1610066	221018
U1610072	221024
U1610073	221015
U1610081	221014
U1610092	221048
U1610097	221010
U1610101	221037
U1610103	221059
U1610155	221049
U1610169	221025
U1610179	221056
U1610184	221058
U1610186	221050
U1610190	221023
U1610202	221045
U1610205	221062
U1610209	221006
U1610210	221032
U1610232	221009
U1610234	221040
U1610238	221060
U1610243	221034
U1610258	221005
U1610264	221055
U1610265	221016
U1610279	221052
U1610287	221035
U1610288	221036
U1610293	221053
U1610300	221027
U1610324	221031
U1610354	221057
U1610381	221030
U1610386	221022
U1610392	221029
U1610399	221046
U1610401	221021
U1610405	221047
U1610407	221007
U1610408	221042
U1610411	221012
U1610414	221001
U1610464	221020
U1610476	221004
U1610489	221054
U1610527	221003
U1610535	221033
U1610577	221043
U1610587	221013
U1610606	221061
U1610614	221002
U1610619	221041
U1610002	222048
U1610004	222009
U1610045	222024
U1610049	222051
U1610053	222018
U1610058	222028
U1610061	222046
U1610062	222025
U1610098	222015
U1610104	222012
U1610119	222019
U1610129	222045
U1610130	222001
U1610131	222007
U1610139	222017
U1610153	222026
U1610157	222030
U1610173	222004
U1610181	222029
U1610189	222010
U1610198	222035
U1610207	222052
U1610212	222008
U1610214	222041
U1610225	222044
U1610229	222054
U1610242	222055
U1610251	222059
U1610269	222014
U1610294	222039
U1610301	222021
U1610307	222058
U1610314	222056
U1610329	222049
U1610343	222034
U1610363	222060
U1610369	222057
U1610400	222023
U1610418	222042
U1610445	222038
U1610454	222006
U1610461	222020
U1610462	222027
U1610472	222043
U1610490	222047
U1610492	222003
U1610529	222002
U1610556	222031
U1610557	222040
U1610559	222036
U1610560	222013
U1610582	222011
U1610586	222005
U1610589	222037
U1610591	222032
U1610592	222053
U1610593	222033
U1610595	222050
U1610607	222022
U1610617	222016
U1610618	222061
U1610003	223051
U1610025	223032
U1610031	223042
U1610034	223033
U1610037	223025
U1610042	223037
U1610050	223017
U1610052	223052
U1610074	223018
U1610080	223044
U1610094	223034
U1610111	223031
U1610116	223020
U1610117	223022
U1610118	223058
U1610120	223028
U1610126	223038
U1610137	223015
U1610142	223005
U1610144	223056
U1610163	223011
U1610168	223045
U1610180	223043
U1610183	223046
U1610193	223009
U1610197	223040
U1610217	223055
U1610260	223023
U1610266	223053
U1610276	223048
U1610289	223027
U1610315	223008
U1610327	223006
U1610349	223041
U1610358	223004
U1610368	223007
U1610388	223050
U1610390	223047
U1610415	223024
U1610416	223003
U1610419	223057
U1610424	223029
U1610440	223035
U1610448	223049
U1610453	223026
U1610475	223014
U1610488	223019
U1610534	223002
U1610538	223010
U1610539	223060
U1610541	223021
U1610542	223013
U1610544	223039
U1610545	223036
U1610547	223054
U1610549	223012
U1610566	223059
U1610571	223030
U1610598	223001
U1610605	223016
121384	421008
121600	421055
121606	421021
U1310169	421053
U1310205	421037
U1310243	421054
U1310280	421019
U1310587	421045
U1310605	421031
U1410004	421004
U1410047	421048
U1410051	421035
U1410054	421014
U1410067	421007
U1410069	421018
U1410084	421030
U1410120	421038
U1410121	421039
U1410124	421003
U1410144	421058
U1410145	421049
U1410150	421005
U1410164	421056
U1410170	421022
U1410173	421047
U1410181	421065
U1410186	421046
U1410192	421040
U1410210	421025
U1410224	421034
U1410237	421052
U1410251	421028
U1410254	421024
U1410259	421013
U1410260	421026
U1410281	421042
U1410285	421063
U1410286	421060
U1410328	421029
U1410354	421017
U1410390	421061
U1410396	421032
U1410404	421036
U1410408	421023
U1410428	421033
U1410429	421016
U1410439	421067
U1410440	421044
U1410443	421012
U1410445	421011
U1410461	421069
U1410478	421002
U1410502	421009
U1410506	421027
U1410509	421068
U1410547	421059
U1410549	421001
U1410558	421006
U1410563	421062
U1410576	421050
U1410605	421020
U1520005	421064
U1520022	421010
U1520024	421066
U1520025	421051
U1520028	421015
U1520038	421057
U1520125	421043
U1520169	421041
121318	422047
U1310027	422062
U1310132	422046
U1310340	422009
U1410072	422060
U1410092	422021
U1410107	422016
U1410114	422043
U1410122	422036
U1410125	422065
U1410139	422041
U1410142	422029
U1410151	422024
U1410175	422057
U1410178	422068
U1410201	422025
U1410215	422003
U1410219	422019
U1410225	422031
U1410243	422040
U1410265	422067
U1410270	422001
U1410271	422007
U1410273	422042
U1410274	422018
U1410290	422011
U1410294	422052
U1410302	422066
U1410311	422050
U1410315	422008
U1410318	422048
U1410321	422053
U1410345	422037
U1410351	422059
U1410372	422035
U1410381	422028
U1410385	422002
U1410431	422049
U1410456	422023
U1410465	422044
U1410475	422013
U1410481	422010
U1410495	422026
U1410522	422034
U1410535	422064
U1410541	422054
U1410551	422005
U1410557	422022
U1410577	422014
U1410603	422020
U1410608	422027
U1410629	422055
U1520006	422039
U1520017	422056
U1520020	422063
U1520023	422045
U1520034	422061
U1520081	422004
U1520096	422058
U1520113	422032
U1520119	422006
U1520123	422038
U1520128	422012
U1520186	422033
U1520219	422030
U1520238	422015
U1520251	422017
U1520259	422051
111154	423020
111711	423012
121330	423060
121585	423062
U1310095	423018
U1310278	423043
U1310360	423013
U1310455	423032
U1310461	423005
U1310546	423066
U1310590	423040
U1310601	423030
U1410002	423002
U1410003	423021
U1410015	423035
U1410025	423052
U1410032	423004
U1410040	423044
U1410048	423046
U1410074	423039
U1410075	423068
U1410126	423006
U1410149	423045
U1410154	423016
U1410196	423019
U1410204	423058
U1410231	423036
U1410246	423009
U1410255	423048
U1410256	423025
U1410284	423050
U1410287	423034
U1410288	423038
U1410295	423053
U1410297	423067
U1410305	423055
U1410308	423047
U1410316	423003
U1410319	423010
U1410349	423061
U1410355	423033
U1410357	423023
U1410360	423059
U1410361	423027
U1410409	423022
U1410417	423063
U1410419	423049
U1410450	423042
U1410488	423001
U1410545	423007
U1410548	423064
U1410572	423041
U1410579	423015
U1410594	423051
U1410604	423024
U1410612	423031
U1410614	423054
U1520015	423057
U1520018	423037
U1520037	423008
U1520066	423011
U1520079	423029
U1520147	423026
U1520150	423056
U1520153	423065
U1520168	423028
U1520177	423014
U1520244	423017
test	322050'''
gr_roll_dict = {}
for each in gr_roll.split('\n'):
    splitted = each.split('\t')
    gr_roll_dict[splitted[0]] = splitted[1]


class FacultySubjectForm(forms.ModelForm):
    faculty = forms.ChoiceField(
        choices=[]
    )

    subject = forms.ChoiceField(
        choices=[]
    )

    division = forms.ChoiceField(
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        super(FacultySubjectForm, self).__init__(*args, **kwargs)
        self.fields['faculty'] = forms.ChoiceField(
            choices=[(i.pk, i.initials) for i in Faculty.objects.all()]
        )

        self.fields['subject'] = forms.ChoiceField(
            choices=[(i.pk, i.short_form) for i in Subject.objects.filter(is_active=True)]
        )

        self.fields['division'] = forms.ChoiceField(
            choices=[(i.pk, i) for i in Division.objects.filter(is_active=True)]
        )

        for field in self.fields:
            if field in ['subject']:
                self.fields[field].widget.attrs.update({'onchange': 'checkElective()'})
            self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = FacultySubject
        fields = '__all__'
        exclude = ['faculty', 'subject', 'division', 'is_active']


class StudentForm(forms.ModelForm):
    current_country = forms.ChoiceField(
        choices=countries
    )
    permanent_country = forms.ChoiceField(
        choices=countries
    )
    email = forms.EmailField()
    # state_choices = states[0].split(',')
    # current_state = forms.ChoiceField(choices=state_choices)
    # permanent_state = forms.ChoiceField(choices=state_choices)
    widgets = {
        'DOB': forms.DateInput(attrs={'class': 'datepicker'})
    }
    # Setting branch only as Comp and Mech for VU
    programme = forms.ChoiceField(choices=[('B.Tech', 'B.Tech'),
                                           ('M.Tech', 'M.Tech')])
    # branch = forms.ChoiceField(
    #     choices=[('Computer', 'Computer'), ('IT', 'IT'), ('EnTC', 'EnTC'), ('Mechanical', 'Mechanical'),
    #              ('Civil', 'Civil')])
    admission_type = forms.ChoiceField(
        choices=[('CAP-I', 'CAP-I'), ('CAP-II', 'CAP-II'), ('CAP-III', 'CAP-III'), ('CAPIV', 'CAPIV'),
                 ('Institute Level', 'Institute Level')]
    )

    batch = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Eg: A1'})
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['DOB', 'handicapped']:
                self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = Student
        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'datepicker form-control'}),
        }
        fields = '__all__'
        exclude = ['salary', 'user', 'branch','year','division','shift']

    # def clean_gr_number(self):
    #     cleaned_data = super().clean()
    #     gr_number = cleaned_data['gr_number']
    #     if not gr_number in gr_roll_dict:
    #         raise forms.ValidationError(
    #             'Your GR Number is not available in our database.\nContact us at viitdevs@gmail.com')
    #
    #     return gr_number


class FacultyForm(forms.ModelForm):
    permanent_country = forms.ChoiceField(
        choices=countries
    )
    current_country = forms.ChoiceField(
        choices=countries
    )
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['DOB', 'teaching_from']:
                self.fields[field].widget.attrs.update({'class': 'form-control', })

    class Meta:
        model = Faculty
        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'datepicker form-control'}),
            'teaching_from': forms.DateInput(attrs={'class': 'datepicker form-control'})
        }
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    # branch = forms.ChoiceField(
    #     choices=[(i.branch, i.branch) for i in Branch.objects.all()])
    # year = forms.ChoiceField(
    #     choices=[(i.year, i.year) for i in year_list]
    # )
    #
    # semester = forms.ChoiceField(
    #     choices=[(i.semester, i.semester) for i in Semester.objects.all()]
    # )
    #
    # type = forms.ChoiceField(
    #     choices=[('Regular', 'Regular'), ('Elective', 'Elective')],
    # )

    is_practical = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['type']:
                self.fields[field].widget.attrs.update({'onchange': 'showElectiveGroup()'})
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['year'] = forms.ChoiceField(
            choices=[(i.year, i.year) for i in CollegeYear.objects.all()]
        )

        self.fields['semester'] = forms.ChoiceField(
            choices=[(i.semester, i.semester) for i in Semester.objects.all()]
        )
        self.fields['branch'] = forms.ChoiceField(
            choices=[(i.branch, i.branch) for i in Branch.objects.all()]
        )

    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['is_active']


class DateScheduleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DateScheduleForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = Schedulable.objects.filter(is_active=True)

        for field in self.fields:
            if field not in ['start_date', 'end_date']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                # self.fields[field].widget.attrs.update({})

    class Meta:
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                'autocomplete': 'off'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'datepicker form-control',
                'autocomplete': 'off'
            }),
        }
        model = Schedule
        fields = '__all__'
        exclude = ['is_active']


class YearBranchSemForm(forms.Form):
    # branch = forms.ChoiceField(
    #     choices=[(i.pk, i.branch) for i in Branch.objects.all()])

    # year = forms.ChoiceField(
    #     choices=[(i.pk, i.year) for i in year_list]
    # )

    # semester = forms.ChoiceField(
    #     choices=[(i.pk, i.semester) for i in Semester.objects.all()]
    # )

    def __init__(self, *args, **kwargs):
        super(YearBranchSemForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['start_date', 'end_date']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['year'] = forms.ChoiceField(
            choices=[(i.pk, i.year) for i in CollegeYear.objects.all()]
        )

        self.fields['semester'] = forms.ChoiceField(
            choices=[(i.pk, i.semester) for i in Semester.objects.all()])
        self.fields['branch'] = forms.ChoiceField(
            choices=[(i.branch, i.branch) for i in Branch.objects.all()]
        )
