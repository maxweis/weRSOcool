from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member

class MemberCreationForm(UserCreationForm):
    ACAD_YEAR_CHOICES = [
            'Freshman',
            'Sophomore',
            'Junior',
            'Senior',
            'Graduate',
    ]

    MAJOR_CHOICES = ['Accountancy - BUS', 'ACES Undeclared - ACES', 'Acting - FAA', 'Actuarial Science - LAS', 'Advertising - COM', 'Aerospace Engineering -\
 ENG', 'African American Studies - LAS', 'Agri-Accounting - ACES', 'Agribusiness, Markets & Management - ACES', 'Agricultural & Biologi\
cal Engineering - ENG', 'Agricultural & Biological Engineering - ACES', 'Agricultural & Consumer Economics - ACES', 'Agricultural Commu\
nications - ACES', 'Agricultural Leadership Education - ACES', 'Agricultural Science Education - ACES', 'Animal Sciences - ACES', 'Anth\
ropology - LAS', 'Architectural Studies - FAA', 'Art Education (K-12) - FAA', 'Art History - LAS', 'Asian American Studies - LAS', 'Ast\
ronomy - LAS', 'Atmospheric Sciences - LAS', 'Biochemistry - LAS', 'Bioengineering - ENG', 'Biology - LAS', 'Chemical & Biomolecular En\
gineering - LAS', 'Chemistry - LAS', 'Civil Engineering - ENG', 'Classics - LAS', 'Communication - LAS', 'Community Health - AHS', 'Com\
parative & World Literature - LAS', 'Computer Engineering - ENG', 'Computer Science - ENG', 'Computer Science & Advertising - COM', 'Co\
mputer Science & Anthropology - LAS', 'Computer Science & Astronomy - LAS', 'Computer Science & Chemistry - LAS', 'Computer Science & C\
rop Sciences - ACES', 'Computer Science & Economics - LAS', 'Computer Science & Geography & Geographic Information Science - LAS', 'Com\
puter Science & Linguistics - LAS', 'Computer Science & Music - FAA', 'Computer Science & Philosophy - LAS', 'Consumer Economics & Fina\
nce - ACES', 'Costume Design & Technology - FAA', 'Crafts: Metal (Jewelry Design) - FAA', 'Creative Writing - LAS', 'Crop Sciences - AC\
ES', 'Dance - FAA', 'Dietetics - ACES', 'Early Childhood Education (Birth-Grade 2) - EDU', 'Earth, Society & Environmental Sustainabili\
ty - LAS', 'East Asian Languages & Cultures - LAS', 'Econometrics & Quantitative Economics - LAS', 'Economics - LAS', 'Electrical Engin\
eering - ENG', 'Elementary Education (Grades 1-6) - EDU', 'Engineering Mechanics - ENG', 'English - LAS', 'Environmental Economics & Po\
licy - ACES', 'Farm Management - ACES', 'Finance - BUS', 'Finance in Agri-Business - ACES', 'Financial Planning - ACES', 'Food Science \
- ACES', 'Food Science & Human Nutrition - ACES', 'French - LAS', 'Gender &\
  Women\'s Studies - LAS', 'Geography & Geographic Information\
 Science - LAS', 'Geology - LAS', 'Germanic Studies - LAS', 'Global Studies - LAS', 'Graphic Design - FAA', 'Health Sciences, Interdisc\
iplinary - AHS', 'History - LAS', 'History of Art - FAA', 'Hospitality Management - ACES', 'Human Development & Family Studies - ACES',
 'Human Nutrition - ACES', 'Industrial Design - FAA', 'Industrial Engineering - ENG', 'Information Systems - BUS', 'Integrative Biology\
 - LAS', 'Interdisciplinary Studies - LAS', 'Italian - LAS', 'Jazz Performance - FAA', 'Journalism - COM', 'Kinesiology - AHS', 'Landsc\
ape Architecture - FAA', 'Latin American Studies - LAS', 'Latina/Latino Studies - LAS', 'Learning & Education Studies - EDU', 'Lighting\
 Design - FAA', 'Linguistics - LAS', 'Lyric Theatre - FAA', 'Management - BUS', 'Marketing - BUS', 'Materials Science & Engineering - E\
NG', 'Mathematics - LAS', 'Mathematics & Computer Science - LAS', 'Mechanical Engineering - ENG', 'Media & Cinema Studies - COM', 'Midd\
le Grades Education (Grades 5-8) - EDU', 'Molecular & Cellular Biology - LAS', 'Music - FAA', 'Music Composition Theory - FAA', 'Music \
Education (K-12) - FAA', 'Music Instrumental Performance - FAA', 'Music Open Studies - FAA', 'Music Voice Performance - FAA', 'Musicolo\
gy - FAA', 'Natural Resources & Environmental Sciences - ACES', 'New Media - FAA', 'Nuclear, Plasma & Radiological Engineering - ENG', 
'Operations Management - BUS', 'Painting - FAA', 'Philosophy - LAS', 'Photography - FAA', 'Physics - LAS', 'Physics, Engineering - ENG'\
, 'Policy, International Trade & Development - ACES', 'Political Science - LAS', 'Portuguese - LAS', 'Psychology - LAS', 'Public Policy\
 & Law - ACES', 'Recreation, Sport & Tourism - AHS', 'Religion - LAS', 'Russian, East European & Eurasian Studies - LAS', 'Scenic Desig\
n - FAA', 'Scenic Technology - FAA', 'Sculpture - FAA', 'Secondary Education - LAS', 'Secondary Education: Agricultural - ACES', 'Secon\
dary Education: Biology - LAS', 'Secondary Education: Chemistry - LAS', 'Secondary Education: Earth Science - LAS', 'Secondary Educatio\
n: English - LAS', 'Secondary Education: Mathematics - LAS', 'Secondary Education: Physics - LAS', 'Secondary Education: Social Studies\
 - LAS', 'Slavic Studies - LAS', 'Social Work - SSW', 'Sociology - LAS', 'Sound\
   Design & Technology - FAA', 'Spanish - LAS', 'Special Education - EDU', 'Speech & Hearing Science - AHS', 'Stage Management - FAA', 'Statistics - LAS', 'Statistics & Computer Science - LAS',
 'Studio Art (BA) - FAA', 'Supply Chain Management - BUS', 'Systems Engineering and Design - ENG', 'Teacher Education: French (K-12) -\
LAS', 'Teacher Education: German (K-12) - LAS', 'Teacher Education: Japanese (K-12) - LAS', 'Teacher Education: Kinesiology - Physical\
Education (K-12) - AHS', 'Teacher Education: Latin (K-12) - LAS', 'Teacher Education: Mandarin Chinese (K-12) - LAS', 'Teacher Educatio\
n: Spanish (K-12) - LAS', 'Technical Systems Management - ACES', 'Theatre Studies - FAA', 'Undeclared - DGS', 'Urban Studies & Planning\
 - FAA']


    user = UserCreationForm()
    major = forms.ChoiceField(choices=[(x,x) for x in MAJOR_CHOICES])
    academic_year = forms.ChoiceField(choices=[(x,x) for x in ACAD_YEAR_CHOICES])
    resume = forms.FileField(required=False)
    icon = forms.ImageField(required=False)

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'major', 'academic_year', 'resume', 'icon', 'password1', 'password2')


class EditProfileForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ('email', 'first_name', 'last_name', 'academic_year', 'major', 'resume', 'icon')
