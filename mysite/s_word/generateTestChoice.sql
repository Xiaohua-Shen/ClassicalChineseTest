# generate pinyin test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'拼音', b.pinyin, a.pinyin=b.pinyin 
    from s_word_sword a, 
        (select sword, pinyin from s_word_sword where pinyin<>"" group by sword, pinyin having count(*)>1) b 
    where a.sword=b.sword;
# generate word_class test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'词性', b.word_class, a.word_class=b.word_class 
    from s_word_sword a, 
        (select sword, word_class from s_word_sword group by sword, word_class having count(*)>1) b 
    where a.sword=b.sword;
# generate meaning test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'含义', b.meaning||'【'||b.word_class||'】', b.meaning||'【'||b.word_class||'】'=a.meaning||'【'||a.word_class||'】'
    from s_word_sword a, 
        (select sword, meaning, word_class from s_word_sword group by sword, meaning, word_class having count(*)>1 ) b 
    where a.sword=b.sword;