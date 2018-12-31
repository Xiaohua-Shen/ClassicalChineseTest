# generate pinyin test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'拼音', b.pinyin, a.pinyin=b.pinyin 
    from s_word_sword a, 
        (select distinct sword, pinyin from s_word_sword where pinyin<>"" ) b,
        (select sword from s_word_sword where pinyin<>"" group by sword having count(distinct pinyin)>1) c
    where a.sword=b.sword
    and b.sword=c.sword
    and a.sample<>"";
# generate word_class test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'词性', b.word_class, a.word_class=b.word_class 
    from s_word_sword a, 
        (select distinct sword, word_class from s_word_sword) b,
        (select sword from s_word_sword group by sword having count(distinct word_class)>1) c
    where a.sword=b.sword
    and b.sword=c.sword
    and a.sample<>"";
# generate meaning test
insert into s_word_swordtest1choice(sword_id, test_type, choice_txt, is_correct) 
    select a.id,'含义', b.meaning||'【'||b.word_class||'】', b.meaning||'【'||b.word_class||'】'=a.meaning||'【'||a.word_class||'】'
    from s_word_sword a, 
        (select distinct sword, meaning, word_class from s_word_sword ) b ,
        (select sword from s_word_sword group by sword having count(distinct meaning)>1) c
    where a.sword=b.sword
    and b.sword=c.sword
    and a.sample<>"";