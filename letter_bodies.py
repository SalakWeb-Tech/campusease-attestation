# letter_bodies.py
# All 32 letter bodies. Each body is 150-180 words.
# The engine picks one at random and combines it with a random layout.

LETTER_BODIES = [
    {
        "id": 1,
        "tone": "Formal/Legal",
        "body": """I, {{parent_title}} {{parent_name}}, do hereby formally attest and confirm that {{student_name}} is my biological {{relationship_term}}. {{subject_pronoun}} has been under my direct care, supervision, and guidance since birth, and I have observed {{possessive_pronoun_lower}} conduct, attitude, and general behavior closely over the years. I have no doubt about {{possessive_pronoun_lower}} identity and background.

I further affirm that {{student_name}} possesses the requisite character and academic preparedness to excel at {{institution_name}}. {{subject_pronoun}} has always exhibited profound respect for constituted authority and a genuine commitment to {{possessive_pronoun_lower}} studies. {{subject_pronoun}} has never been involved in any criminal or disciplinary issues, and {{possessive_pronoun_lower}} moral standing within our family and community remains unquestionable.

I hereby vouch for {{object_pronoun}} with full legal responsibility. {{subject_pronoun}} will comply with all rules, regulations, and codes of conduct of {{institution_name}}. I pledge {{possessive_pronoun_lower}} continued support to ensure {{subject_pronoun_lower}} upholds the values of the university. I make this attestation in good faith and for the benefit of the institution.""",
    },
    {
        "id": 2,
        "tone": "Warm/Parental",
        "body": """It is with immense joy and a heart full of gratitude that I write to attest to the character of my beloved {{relationship_term}}, {{student_name}}. Raising {{object_pronoun}} has been a blessing, and I have watched {{object_pronoun}} grow into a respectful and diligent young adult. {{subject_pronoun}} has never been involved in any negative activity, and {{possessive_pronoun_lower}} conduct at home has always been exemplary.

{{subject_pronoun}} is a God-fearing individual who values honesty and hard work above all else. At home, {{subject_pronoun_lower}} performs {{possessive_pronoun_lower}} chores diligently and relates peacefully with siblings and neighbors. I am confident that {{subject_pronoun_lower}} will bring the same level of dedication and humility to {{institution_name}} that {{subject_pronoun_lower}} has always shown at home.

As the {{parent_title}} of {{student_name}}, I assure the university that {{student_name}} is a person of integrity. {{subject_pronoun}} respects elders and authority figures and will comply with all campus regulations. I have no doubt that {{subject_pronoun_lower}} will make both our family and the institution proud. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 3,
        "tone": "Character/Integrity-focused",
        "body": """This letter serves to confirm that {{student_name}}, my {{relationship_term}}, is a person of unquestionable integrity and high moral standing. I have observed {{object_pronoun}} closely over the years and can testify to {{possessive_pronoun_lower}} unwavering commitment to truth and honesty. {{subject_pronoun}} has consistently displayed honesty, humility, and godliness in all {{possessive_pronoun_lower}} dealings.

{{subject_pronoun}} is known for {{possessive_pronoun_lower}} calm demeanor and respectful nature. Throughout {{possessive_pronoun_lower}} formative years, {{subject_pronoun_lower}} has never been associated with any negative vices or behavior capable of tarnishing the image of {{institution_name}}. {{subject_pronoun}} relates peacefully with peers, elders, and community members at all times.

I confirm that {{student_name}} is obedient and cooperative. {{subject_pronoun}} understands the importance of rules and regulations and obeys constituted authority without resistance. I fully support {{possessive_pronoun_lower}} admission and pray for {{possessive_pronoun_lower}} success in all academic endeavors. {{subject_pronoun}} is a reliable and trustworthy individual, and I make this attestation in good faith.""",
    },
    {
        "id": 4,
        "tone": "Academic Focus",
        "body": """I write to attest to the academic potential and intellectual capacity of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} has always been a focused learner, demonstrating a keen interest in acquiring knowledge and skills relevant to {{possessive_pronoun_lower}} chosen field. {{possessive_pronoun}} dedication to excellence is evident in {{possessive_pronoun_lower}} consistent performance and serious attitude towards learning.

{{subject_pronoun}} possesses a disciplined approach to studies and has shown the resilience required to succeed in a rigorous environment like {{institution_name}}. {{subject_pronoun}} manages time wisely, prioritizes academic work, and respects teachers and follows instructions diligently. I have observed {{possessive_pronoun_lower}} study habits and can confirm that {{subject_pronoun_lower}} is serious and determined.

I attest that {{student_name}} is well-prepared for the challenges of university life. {{subject_pronoun}} is respectful to teachers and peers alike and eager to learn. I am confident {{subject_pronoun_lower}} will contribute positively to the academic community at {{institution_name}}. I pledge my support to ensure {{subject_pronoun_lower}} excels in {{possessive_pronoun_lower}} chosen field and makes us proud.""",
    },
    {
        "id": 5,
        "tone": "Traditional/Civic",
        "body": """As a respected member of the community and the parent of {{student_name}}, I hereby attest to the good conduct and civic responsibility of my {{relationship_term}}. {{subject_pronoun}} was raised with strong cultural values and respect for communal norms. {{subject_pronoun}} is known for {{possessive_pronoun_lower}} humility and obedience, and {{subject_pronoun_lower}} is a person of high repute in our locality.

{{student_name}} is known within our locality as a humble and obedient young person. {{subject_pronoun}} has never been found wanting in character or social behavior. {{possessive_pronoun}} dealings with neighbors and community members have always been cordial and respectful. {{subject_pronoun}} participates in community activities and shows respect for elders and traditional institutions.

I vouch for {{object_pronoun}} as a worthy ambassador of our home to {{institution_name}}. {{subject_pronoun}} will adhere to all rules and regulations and represent our family positively. I pledge my support to ensure {{subject_pronoun_lower}} remains disciplined and focused. I pray for {{possessive_pronoun_lower}} success and good conduct. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 6,
        "tone": "Formal/Legal",
        "body": """I, {{parent_title}} {{parent_name}}, being of sound mind, do hereby attest to the identity and good character of my {{relationship_term}}, {{student_name}}. I confirm that {{subject_pronoun}} is a person of good repute and has no history of criminal behavior or social misconduct. {{subject_pronoun}} has been under my direct care and supervision since birth, and I have no doubt about {{possessive_pronoun_lower}} identity and background.

{{subject_pronoun}} has been raised with strict adherence to moral values and ethical standards. I guarantee that {{subject_pronoun_lower}} will abide by the rules and regulations of {{institution_name}} and contribute to the peace and order of the campus. {{subject_pronoun}} respects constituted authority and follows instructions without resistance. {{subject_pronoun}} relates peacefully with peers and community members at all times.

I take full responsibility for {{possessive_pronoun_lower}} actions and pledge to support the university in ensuring {{subject_pronoun_lower}} remains a disciplined student. {{subject_pronoun}} is respectful and law-abiding. I make this attestation in good faith for the benefit of the institution. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 7,
        "tone": "Warm/Parental",
        "body": """I am writing to express my profound pride in my {{relationship_term}}, {{student_name}}, and to attest to {{possessive_pronoun_lower}} admirable character. {{subject_pronoun}} is a source of joy to our family, known for {{possessive_pronoun_lower}} gentle spirit and willingness to help others. {{subject_pronoun}} has never been involved in any negative activity, and {{possessive_pronoun_lower}} conduct at home has always been exemplary.

{{subject_pronoun}} has always been an obedient child who respects constituted authority, both at home and in the community. At home, {{subject_pronoun_lower}} performs {{possessive_pronoun_lower}} chores diligently and relates peacefully with siblings and neighbors. I am confident that {{subject_pronoun_lower}} will carry these virtues into {{institution_name}} and excel in {{possessive_pronoun_lower}} studies. {{possessive_pronoun}} attitude towards learning is serious and focused.

I assure the institution that {{student_name}} is well-behaved and morally upright. Please accept this attestation as a testimony of {{possessive_pronoun_lower}} readiness for higher education. I pledge my full support to ensure {{subject_pronoun_lower}} succeeds academically and socially. I have no doubt {{subject_pronoun_lower}} will make us proud. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 8,
        "tone": "Character/Integrity-focused",
        "body": """I hereby certify that {{student_name}} is my {{relationship_term}} and a person of exemplary character. I have known {{object_pronoun}} all {{possessive_pronoun_lower}} life, and {{subject_pronoun_lower}} has consistently displayed traits of honesty, humility, and godliness. {{subject_pronoun}} is a person of high moral standing, and {{possessive_pronoun_lower}} integrity is beyond question.

{{subject_pronoun}} is not given to violence or any form of deviant behavior. {{possessive_pronoun}} respect for constituted authority is unwavering, and {{subject_pronoun_lower}} obeys rules without resistance. I confirm that {{subject_pronoun_lower}} has never been associated with any negative vice or criminal activity. {{subject_pronoun}} relates peacefully with others at all times and treats everyone with respect.

I vouch for {{possessive_pronoun_lower}} integrity and pledge my full support to the university administration. {{subject_pronoun}} is a reliable and trustworthy individual who will be a positive influence on campus. I make this attestation in good faith. {{subject_pronoun}} is a worthy candidate for higher education, and I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 9,
        "tone": "Academic Focus",
        "body": """I write to confirm the academic readiness and intellectual curiosity of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} has always been a diligent student, showing a remarkable commitment to {{possessive_pronoun_lower}} educational pursuits. {{possessive_pronoun}} study habits are disciplined and focused, and {{subject_pronoun_lower}} manages time wisely while prioritizing academic work.

{{subject_pronoun}} possesses the discipline required to navigate the academic rigors of {{institution_name}}. I have observed {{possessive_pronoun_lower}} study habits and can attest that {{subject_pronoun_lower}} is focused and determined to succeed. {{subject_pronoun}} respects teachers, follows academic instructions diligently, and is always well-prepared for the challenges ahead. {{subject_pronoun}} is a very hardworking and dedicated learner.

I confirm that {{student_name}} is obedient to instructions and eager to learn. {{subject_pronoun}} will surely make good use of this admission opportunity. I pledge my full and complete support to ensure {{subject_pronoun_lower}} excels in {{possessive_pronoun_lower}} chosen field. I have no doubt about {{possessive_pronoun_lower}} success and therefore fully endorse {{object_pronoun}} for this academic journey.""",
    },
    {
        "id": 10,
        "tone": "Traditional/Civic",
        "body": """I, {{parent_title}} {{parent_name}}, a stakeholder in the community, do hereby attest to the uprightness of {{student_name}}, my {{relationship_term}}. In our society, {{subject_pronoun}} is recognized as a respectful and well-cultured individual. {{subject_pronoun}} has been taught the values of honesty and respect for elders, and {{subject_pronoun_lower}} conduct has always been exemplary in every setting.

{{subject_pronoun}} has consistently demonstrated respect for communal norms and traditional institutions. {{possessive_pronoun}} dealings with neighbors and community members have always been cordial and respectful. {{subject_pronoun}} participates in community activities and shows regard for elders. I have no doubt that {{subject_pronoun_lower}} will represent our family and community well at {{institution_name}}.

I vouch for {{possessive_pronoun_lower}} character and confirm that {{subject_pronoun_lower}} has no history of delinquency. {{subject_pronoun}} is a worthy candidate for higher education and will adhere to all rules and regulations. I pledge my support to ensure {{subject_pronoun_lower}} remains disciplined and focused. I pray for {{possessive_pronoun_lower}} success and good conduct. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 11,
        "tone": "Formal/Legal",
        "body": """This is to formally attest that {{student_name}} is my biological {{relationship_term}}. I confirm that {{subject_pronoun}} is of good moral standing and has never been convicted of any offence. {{possessive_pronoun}} records are clean, and {{possessive_pronoun_lower}} background is beyond reproach. {{subject_pronoun}} has been under my direct care and supervision since birth, and I have no doubt about {{possessive_pronoun_lower}} identity.

I assure {{institution_name}} that {{student_name}} will comply with all matriculation regulations and codes of conduct. {{subject_pronoun}} has been raised to respect rules and order, and {{subject_pronoun_lower}} obeys constituted authority without resistance. {{subject_pronoun}} relates peacefully with peers and community members at all times. I confirm that {{subject_pronoun_lower}} has never been associated with any criminal activity or gross misconduct.

I hereby pledge my support to ensure {{subject_pronoun_lower}} completes {{possessive_pronoun_lower}} program without any disciplinary issues. {{subject_pronoun}} is respectful and law-abiding. I make this attestation in good faith and for the benefit of the institution. I therefore fully endorse {{object_pronoun}} for admission and wish {{object_pronoun}} success in all {{possessive_pronoun_lower}} academic endeavors.""",
    },
    {
        "id": 12,
        "tone": "Warm/Parental",
        "body": """It is a pleasure to write on behalf of my {{relationship_term}}, {{student_name}}. {{subject_pronoun}} is a wonderful young person with a heart full of kindness and a mind eager to learn. I have nurtured {{object_pronoun}} with love and discipline, and {{subject_pronoun_lower}} has grown into a respectful, obedient, and God-fearing young adult. {{subject_pronoun}} is a source of joy to everyone around {{object_pronoun}}.

{{subject_pronoun}} is respectful and obedient to authority. At home, {{subject_pronoun_lower}} performs {{possessive_pronoun_lower}} chores diligently and relates peacefully with siblings and neighbors. {{subject_pronoun}} has never been involved in any negative activity or bad company. I am confident that {{subject_pronoun_lower}} will adapt quickly to the environment at {{institution_name}} and make us proud with {{possessive_pronoun_lower}} conduct and dedication to studies.

I attest to {{possessive_pronoun_lower}} good behavior and pray for {{possessive_pronoun_lower}} success in all {{possessive_pronoun_lower}} academic endeavors. I pledge my full support to ensure {{subject_pronoun_lower}} succeeds academically and socially. I have no doubt {{subject_pronoun_lower}} will represent our family well. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 13,
        "tone": "Character/Integrity-focused",
        "body": """I write to vouch for the integrity and moral uprightness of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} is a person of high moral standards who fears God and respects humanity. I have known {{object_pronoun}} all {{possessive_pronoun_lower}} life, and {{subject_pronoun_lower}} has consistently displayed honesty, humility, and godliness in all {{possessive_pronoun_lower}} dealings with others.

{{subject_pronoun}} has never exhibited traits of aggression or dishonesty. I confirm that {{subject_pronoun_lower}} is reliable and trustworthy. {{possessive_pronoun}} stay at {{institution_name}} will be characterized by good conduct, respect for authority, and peaceful relations with peers and staff. {{subject_pronoun}} obeys rules without resistance and relates with everyone respectfully.

I pledge my support to the university to ensure {{subject_pronoun_lower}} remains a disciplined student. {{subject_pronoun}} is a person of unwavering integrity and will be a positive influence on campus. I make this attestation in good faith, with full confidence in {{possessive_pronoun_lower}} character. {{subject_pronoun}} is a worthy candidate for higher education, and I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 14,
        "tone": "Academic Focus",
        "body": """I attest to the academic capability of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} has demonstrated a strong aptitude for learning and a commitment to academic excellence throughout {{possessive_pronoun_lower}} formative years. {{possessive_pronoun}} dedication to studies is evident in {{possessive_pronoun_lower}} consistent performance and serious attitude towards learning. {{subject_pronoun}} is a diligent and hardworking student.

{{subject_pronoun}} is disciplined and focused on {{possessive_pronoun_lower}} goals. I am confident {{subject_pronoun_lower}} will cope with the demands of {{institution_name}} and excel in {{possessive_pronoun_lower}} chosen field of study. {{subject_pronoun}} manages time wisely, prioritizes academic work, and follows instructions diligently. {{subject_pronoun}} is well-prepared for the rigors of university life.

I confirm {{subject_pronoun_lower}} respect for academic authority and pledge to support {{possessive_pronoun_lower}} educational journey. {{subject_pronoun}} will contribute positively to the academic community and will make good use of every learning opportunity. I have no doubt about {{possessive_pronoun_lower}} success, and I therefore fully endorse {{object_pronoun}} for this academic pursuit.""",
    },
    {
        "id": 15,
        "tone": "Traditional/Civic",
        "body": """I hereby attest to the good character and community standing of {{student_name}}, my {{relationship_term}}. In our community, {{subject_pronoun}} is known for {{possessive_pronoun_lower}} humility and respect for tradition. {{subject_pronoun}} was raised with strong cultural values and has consistently shown regard for elders and communal norms. {{subject_pronoun}} is a person of high repute in our locality.

{{subject_pronoun}} has never brought shame to our family. {{possessive_pronoun}} conduct has always been exemplary, and {{subject_pronoun_lower}} interacts with everyone respectfully. {{subject_pronoun}} participates in community activities and shows regard for traditional institutions. I am confident {{subject_pronoun_lower}} will be a good ambassador at {{institution_name}} and will uphold the values we hold dear.

I vouch for {{possessive_pronoun_lower}} conduct and pray for {{possessive_pronoun_lower}} success. {{subject_pronoun}} will adhere to all rules and regulations and represent our family and community positively. I pledge my support to ensure {{subject_pronoun_lower}} remains disciplined and focused. I make this attestation in good faith. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 16,
        "tone": "Formal/Legal",
        "body": """I, {{parent_title}} {{parent_name}}, do hereby attest that {{student_name}} is my {{relationship_term}}. I confirm {{subject_pronoun}} is of good character and has no criminal record. {{subject_pronoun}} has been under my direct care and supervision since birth, and I have no doubt about {{possessive_pronoun_lower}} identity, background, and moral standing. {{possessive_pronoun}} conduct has always been above reproach.

I guarantee {{possessive_pronoun_lower}} compliance with all university rules. {{subject_pronoun}} is respectful and law-abiding. {{subject_pronoun}} has been raised with strict adherence to moral values and ethical standards, and {{subject_pronoun_lower}} obeys constituted authority without resistance. {{subject_pronoun}} relates peacefully with peers and community members at all times. I confirm {{subject_pronoun_lower}} has never been involved in any criminal activity, violence, or gross misconduct.

I pledge my full support to {{institution_name}} in ensuring {{subject_pronoun_lower}} remains disciplined throughout {{possessive_pronoun_lower}} stay. {{subject_pronoun}} will comply with all rules, regulations, and codes of conduct of the university. I make this attestation in good faith for the benefit of the institution. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 17,
        "tone": "Warm/Parental",
        "body": """I am proud to attest to the character of my {{relationship_term}}, {{student_name}}. {{subject_pronoun}} is a blessing to our family, known for {{possessive_pronoun_lower}} gentle and obedient nature. I have watched {{object_pronoun}} grow with humility and kindness, and {{subject_pronoun_lower}} has consistently shown respect for elders and authority figures. {{subject_pronoun}} is a source of joy to everyone around {{object_pronoun}}.

I am confident {{subject_pronoun_lower}} will excel at {{institution_name}}. {{subject_pronoun}} respects authority and values education. At home, {{subject_pronoun_lower}} performs {{possessive_pronoun_lower}} chores diligently and relates peacefully with siblings and neighbors. {{subject_pronoun}} has never been involved in any negative activity or bad company. {{possessive_pronoun}} attitude towards studies is serious and focused.

I assure the university of {{possessive_pronoun_lower}} good conduct and my continued support. {{subject_pronoun}} will comply with all campus rules and respect constituted authority. I pledge to ensure {{subject_pronoun_lower}} succeeds academically and socially. I have no doubt {{subject_pronoun_lower}} will make us proud. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 18,
        "tone": "Character/Integrity-focused",
        "body": """I certify that {{student_name}} is my {{relationship_term}} and a person of high integrity. {{subject_pronoun}} is honest, godly, and respectful. I have known {{object_pronoun}} all {{possessive_pronoun_lower}} life, and {{subject_pronoun_lower}} has consistently displayed traits of honesty, humility, and godliness in all {{possessive_pronoun_lower}} dealings. {{possessive_pronoun}} moral standing is unquestionable.

I have never known {{object_pronoun}} to engage in any misconduct. {{subject_pronoun}} is not given to violence, dishonesty, or any form of deviant behavior. {{possessive_pronoun}} respect for constituted authority is unwavering, and {{subject_pronoun_lower}} obeys rules without resistance. {{subject_pronoun}} relates peacefully with others at all times and treats everyone with dignity and respect.

I vouch for {{possessive_pronoun_lower}} character and pledge my support to {{institution_name}}. {{subject_pronoun}} will be a positive influence on campus and will uphold the values of discipline and moral uprightness. I make this attestation in good faith. {{subject_pronoun}} is a worthy candidate for higher education, and I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 19,
        "tone": "Academic Focus",
        "body": """I attest to the academic potential of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} is a diligent student with a hunger for knowledge and a genuine commitment to {{possessive_pronoun_lower}} studies. {{possessive_pronoun}} study habits are disciplined, and {{subject_pronoun_lower}} manages time wisely to prioritize academic work. {{subject_pronoun}} is a focused and hardworking learner.

{{subject_pronoun}} is prepared for the rigors of {{institution_name}}. I am confident {{subject_pronoun_lower}} will make excellent grades. {{subject_pronoun}} respects teachers, follows academic instructions diligently, and is always well-prepared for the challenges ahead. {{subject_pronoun}} has demonstrated strong aptitude in {{possessive_pronoun_lower}} previous academic pursuits and possesses the resilience required for university-level study.

I confirm {{subject_pronoun_lower}} obedience to rules and pledge my support for {{possessive_pronoun_lower}} studies. {{subject_pronoun}} will contribute positively to the academic community and will make good use of every learning opportunity. I have no doubt about {{possessive_pronoun_lower}} success, and I therefore fully endorse {{object_pronoun}} for this academic journey.""",
    },
    {
        "id": 20,
        "tone": "Traditional/Civic",
        "body": """I, {{parent_title}} {{parent_name}}, attest to the good conduct of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} is a well-cultured and respectful member of our community. {{subject_pronoun}} was raised with strong cultural values and has consistently shown regard for elders and traditional institutions. {{subject_pronoun}} is a person of high repute in our locality.

{{possessive_pronoun}} conduct has always been exemplary, and {{subject_pronoun_lower}} relates with everyone respectfully. {{subject_pronoun}} participates in community activities and shows regard for communal norms. I am confident {{subject_pronoun_lower}} will represent us well at {{institution_name}} and will uphold the values we hold dear as a family and community.

I vouch for {{possessive_pronoun_lower}} character and pray for {{possessive_pronoun_lower}} success. {{subject_pronoun}} will adhere to all rules and regulations and will represent our family positively. I pledge my support to ensure {{subject_pronoun_lower}} remains disciplined and focused. I make this attestation in good faith. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 21,
        "tone": "Formal/Legal",
        "body": """I, {{parent_title}} {{parent_name}}, hereby formally attest that {{student_name}} is my biological {{relationship_term}}. {{subject_pronoun}} has been under my direct care, supervision, and guidance since birth, and I have observed {{possessive_pronoun_lower}} conduct, attitude, and general behavior closely over the years. I have no doubt about {{possessive_pronoun_lower}} identity and background.

I confirm that {{subject_pronoun_lower}} is disciplined, respectful, and obedient to constituted authority. {{subject_pronoun}} has never been involved in any act of criminality, violence, or gross misconduct. {{possessive_pronoun}} moral standing within our family and community remains unquestionable, and {{subject_pronoun_lower}} relates peacefully with others. {{subject_pronoun}} respects elders and follows instructions without resistance.

I hereby vouch for {{object_pronoun}} with full legal and parental responsibility. {{subject_pronoun}} will comply with all rules, regulations, and codes of conduct of {{institution_name}}. I pledge my continued support to ensure {{subject_pronoun_lower}} upholds the values of discipline, humility, and academic excellence throughout {{possessive_pronoun_lower}} stay. I make this attestation in good faith and for the benefit of the university.""",
    },
    {
        "id": 22,
        "tone": "Warm/Parental",
        "body": """I write with great joy to attest to the character of my dear {{relationship_term}}, {{student_name}}. {{subject_pronoun}} has been a source of pride to our family, growing up with humility, kindness, and a deep respect for elders. I have watched {{object_pronoun}} mature into a responsible young adult. {{subject_pronoun}} has never been involved in any negative activity.

{{subject_pronoun}} is obedient, God-fearing, and always willing to learn. At home, {{subject_pronoun_lower}} performs {{possessive_pronoun_lower}} chores diligently and relates peacefully with siblings and neighbors. I am confident that {{subject_pronoun_lower}} will bring these same virtues to {{institution_name}}. {{possessive_pronoun}} attitude towards studies is serious and focused.

As {{parent_title}} {{parent_name}}, I assure the university that {{student_name}} is well-behaved and morally upright. {{subject_pronoun}} respects constituted authority and will comply with all campus regulations. I pledge my full support to ensure {{subject_pronoun_lower}} succeeds academically and socially. I have no doubt {{subject_pronoun_lower}} will make us proud. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 23,
        "tone": "Formal/Legal",
        "body": """I, {{parent_title}} {{parent_name}}, do hereby solemnly attest that {{student_name}} is my biological {{relationship_term}}. {{subject_pronoun}} has been known to me since birth and has remained under my direct care and supervision. I confirm that {{possessive_pronoun_lower}} identity, background, and family history are true and accurate.

{{subject_pronoun}} is a person of good conduct, humility, and obedience to constituted authority. {{subject_pronoun}} has never been involved in any criminal activity, violence, or immoral behavior. {{possessive_pronoun}} respect for elders and rules is exemplary, and {{subject_pronoun_lower}} relates peacefully with peers and community members. I have no doubt about {{possessive_pronoun_lower}} moral standing.

I hereby solemnly vouch for {{object_pronoun}} with full and complete parental and legal responsibility. {{subject_pronoun}} will comply with all rules, regulations, and codes of conduct of {{institution_name}}. I pledge my continued support to ensure {{subject_pronoun_lower}} upholds discipline, humility, and academic excellence throughout {{possessive_pronoun_lower}} stay. I make this attestation in good faith and for the benefit of the university.""",
    },
    {
        "id": 24,
        "tone": "Warm/Parental",
        "body": """I write with immense joy and gratitude to attest to the character of my beloved {{relationship_term}}, {{student_name}}. {{subject_pronoun}} has been a blessing to our family and has grown into a respectful, obedient, and God-fearing young adult. I have watched {{object_pronoun}} demonstrate humility and kindness daily. {{subject_pronoun}} is a source of joy to everyone around {{object_pronoun}}.

{{subject_pronoun}} is diligent in {{possessive_pronoun_lower}} chores and always willing to learn. At home and in the community, {{subject_pronoun_lower}} respects elders and follows instructions without complaint. {{subject_pronoun}} has never been involved in any negative activity or bad company. {{possessive_pronoun}} moral standing is a source of pride to us. {{subject_pronoun}} is truthful and honest in all {{possessive_pronoun_lower}} dealings.

As {{parent_title}} {{parent_name}}, I assure {{institution_name}} that {{student_name}} is well-behaved and morally upright. {{subject_pronoun}} will comply with all campus rules and respect constituted authority. I pledge my full support to ensure {{subject_pronoun_lower}} succeeds academically and socially. I have no doubt {{subject_pronoun_lower}} will make us proud. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 25,
        "tone": "Character/Integrity-focused",
        "body": """I hereby certify that {{student_name}} is my {{relationship_term}} and a person of exemplary character. {{subject_pronoun}} has consistently displayed honesty, humility, and godliness in all {{possessive_pronoun_lower}} dealings. I have known {{object_pronoun}} all {{possessive_pronoun_lower}} life and can vouch for {{possessive_pronoun_lower}} integrity. {{subject_pronoun}} is a person of high moral standing.

{{subject_pronoun}} is not given to violence, dishonesty, or any form of deviant behavior. {{possessive_pronoun}} respect for constituted authority is unwavering, and {{subject_pronoun_lower}} obeys rules without resistance. I confirm that {{subject_pronoun_lower}} has never been associated with any negative vice or criminal activity. {{subject_pronoun}} is a reliable and trustworthy individual. {{subject_pronoun}} relates peacefully with others at all times.

I vouch for {{object_pronoun}} with full confidence and pledge my support to {{institution_name}}. {{subject_pronoun}} will be a positive influence on campus and will uphold the values of discipline and moral uprightness. I make this attestation in good faith. {{subject_pronoun}} is a worthy candidate for higher education. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 26,
        "tone": "Academic Focus",
        "body": """I write to attest to the academic potential and intellectual capacity of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} has always been a focused learner, demonstrating a keen interest in acquiring knowledge and skills. {{possessive_pronoun}} commitment to studies is evident in {{possessive_pronoun_lower}} consistent performance. {{subject_pronoun}} is a diligent and hardworking student.

{{subject_pronoun}} possesses the discipline and resilience required to succeed in a rigorous environment like {{institution_name}}. {{subject_pronoun}} respects teachers and follows academic instructions diligently. I have observed {{possessive_pronoun_lower}} study habits and can confirm that {{subject_pronoun_lower}} is serious and determined. {{subject_pronoun}} is well-prepared for university challenges. {{subject_pronoun}} manages time wisely and prioritizes academic work.

I confirm that {{student_name}} is obedient to rules and eager to learn. {{subject_pronoun}} will contribute positively to the academic community at {{institution_name}}. I pledge my support to ensure {{subject_pronoun_lower}} excels in {{possessive_pronoun_lower}} chosen field. I have no doubt about {{possessive_pronoun_lower}} success. I therefore fully endorse {{object_pronoun}} for this academic journey.""",
    },
    {
        "id": 27,
        "tone": "Traditional/Civic",
        "body": """I, {{parent_title}} {{parent_name}}, a respected member of our community, hereby attest to the good conduct and civic responsibility of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} was raised with strong cultural values and respect for communal norms. {{subject_pronoun}} is known for {{possessive_pronoun_lower}} humility and obedience. {{subject_pronoun}} is a person of high repute in our locality.

{{subject_pronoun}} has never been found wanting in character or social behavior. {{possessive_pronoun}} interaction with neighbors and community members has always been cordial and respectful. {{subject_pronoun}} participates in community activities and shows respect for elders and traditional institutions. I have no doubt about {{possessive_pronoun_lower}} moral uprightness. {{subject_pronoun}} obeys constituted authority without hesitation.

I vouch for {{object_pronoun}} as a worthy ambassador of our home to {{institution_name}}. {{subject_pronoun}} will adhere to all rules and regulations and represent our family positively. I pledge my support to ensure {{subject_pronoun_lower}} remains disciplined and focused. I pray for {{possessive_pronoun_lower}} success and good conduct. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 28,
        "tone": "Formal/Legal",
        "body": """I, {{parent_title}} {{parent_name}}, do hereby formally attest that {{student_name}} is my biological {{relationship_term}}. {{subject_pronoun}} has been under my direct care and supervision since birth. I confirm that {{possessive_pronoun_lower}} identity and background are true and accurate. {{subject_pronoun}} is a person of good repute. {{subject_pronoun}} is a law-abiding citizen.

{{subject_pronoun}} has never been involved in any criminal activity, violence, or gross misconduct. {{possessive_pronoun}} moral standing within our family and community remains unquestionable. {{subject_pronoun}} respects constituted authority and follows instructions without resistance. I have no doubt about {{possessive_pronoun_lower}} discipline and obedience. {{subject_pronoun}} relates peacefully with peers and neighbors.

I hereby vouch for {{object_pronoun}} with full legal and parental responsibility. {{subject_pronoun}} will comply with all rules, regulations, and codes of conduct of {{institution_name}}. I pledge my continued support to ensure {{subject_pronoun_lower}} upholds discipline, humility, and academic excellence. I make this attestation in good faith for the benefit of the university. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 29,
        "tone": "Warm/Parental",
        "body": """I write with a heart full of pride to attest to the character of my dear {{relationship_term}}, {{student_name}}. {{subject_pronoun}} has been a source of joy to our family, growing up with humility, kindness, and respect for elders. I have watched {{object_pronoun}} mature into a responsible and obedient young adult. {{subject_pronoun}} is a blessing to everyone around {{object_pronoun}}.

{{subject_pronoun}} is God-fearing and always willing to learn. At home, {{subject_pronoun_lower}} performs {{possessive_pronoun_lower}} chores diligently and relates peacefully with siblings and neighbors. {{subject_pronoun}} has never been involved in any negative activity or bad company. {{possessive_pronoun}} attitude towards studies is serious and focused. {{subject_pronoun}} is truthful and honest in all {{possessive_pronoun_lower}} dealings.

As {{parent_title}} {{parent_name}}, I assure {{institution_name}} that {{student_name}} is well-behaved and morally upright. {{subject_pronoun}} respects constituted authority and will comply with all campus regulations. I pledge my full support to ensure {{subject_pronoun_lower}} succeeds academically and socially. I have no doubt {{subject_pronoun_lower}} will make us proud. I therefore vouch for {{object_pronoun}} with full parental confidence.""",
    },
    {
        "id": 30,
        "tone": "Character/Integrity-focused",
        "body": """I hereby certify that {{student_name}} is my {{relationship_term}} and a person of high moral standing. {{subject_pronoun}} has consistently displayed honesty, humility, and godliness in all {{possessive_pronoun_lower}} dealings. I have known {{object_pronoun}} all {{possessive_pronoun_lower}} life and can vouch for {{possessive_pronoun_lower}} integrity. {{subject_pronoun}} is a reliable and trustworthy individual.

{{subject_pronoun}} is not given to violence, dishonesty, or any form of deviant behavior. {{possessive_pronoun}} respect for constituted authority is unwavering, and {{subject_pronoun_lower}} obeys rules without resistance. I confirm that {{subject_pronoun_lower}} has never been associated with any negative vice or criminal activity. {{subject_pronoun}} relates peacefully with others at all times. {{subject_pronoun}} obeys constituted authority without hesitation.

I vouch for {{object_pronoun}} with full confidence and pledge my support to {{institution_name}}. {{subject_pronoun}} will be a positive influence on campus and will uphold the values of discipline and moral uprightness. I make this attestation in good faith. {{subject_pronoun}} is a worthy candidate for higher education. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
    {
        "id": 31,
        "tone": "Academic Focus",
        "body": """I write to attest to the academic potential and intellectual curiosity of {{student_name}}, my {{relationship_term}}. {{subject_pronoun}} has always been a diligent student, demonstrating a keen interest in learning and a commitment to excellence. {{possessive_pronoun}} study habits are disciplined and focused. {{subject_pronoun}} is a very hardworking and dedicated learner.

{{subject_pronoun}} possesses the resilience required to succeed in a rigorous environment like {{institution_name}}. {{subject_pronoun}} respects teachers and follows academic instructions diligently. I have observed {{possessive_pronoun_lower}} performance and can confirm that {{subject_pronoun_lower}} is serious and determined. {{subject_pronoun}} manages time wisely and prioritizes academic work. {{subject_pronoun}} is always well-prepared for university challenges.

I confirm that {{student_name}} is obedient to rules and eager to learn. {{subject_pronoun}} will contribute positively to the academic community at {{institution_name}}. I pledge my full and complete support to ensure {{subject_pronoun_lower}} excels in {{possessive_pronoun_lower}} chosen field. I have no doubt about {{possessive_pronoun_lower}} success. I therefore fully endorse {{object_pronoun}} for this academic journey.""",
    },
    {
        "id": 32,
        "tone": "Traditional/Civic",
        "body": """I, {{parent_title}} {{parent_name}}, a stakeholder in our community, do hereby attest to the uprightness of {{student_name}}, my {{relationship_term}}. In our society, {{subject_pronoun}} is recognized as a respectful and well-cultured individual. {{subject_pronoun}} has been taught the values of honesty and respect for elders. {{subject_pronoun}} is a person of high repute in our locality.

I have no doubt that {{subject_pronoun_lower}} will represent our family and community well at {{institution_name}}. {{possessive_pronoun}} conduct has always been exemplary. {{subject_pronoun}} obeys constituted authority without hesitation. {{subject_pronoun}} always relates peacefully with peers and neighbors. {{subject_pronoun}} shows regard for communal norms and traditional institutions.

I vouch for {{possessive_pronoun_lower}} character and confirm that {{subject_pronoun_lower}} has no history of delinquency. {{subject_pronoun}} is a worthy candidate for higher education. I pledge my support to ensure {{subject_pronoun_lower}} remains disciplined and focused. I pray for {{possessive_pronoun_lower}} success and good conduct at {{institution_name}}. I therefore fully endorse {{object_pronoun}} for admission.""",
    },
]