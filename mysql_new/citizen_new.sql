select
    证照号码
from
    citizen;

select distinct 证照号码
from citizen;


delete from citizen
where 证照号码 = '0';


# 删除证照号码为0的记录
delete
from citizen
where 证照号码 = '0';

# 删除重复的记录



select 证照号码, count(*)
from citizen
group by 证照号码;


select *
from citizen
where 证照号码 = '63212619800108044X';

select 交易卡号, count(*)
from account
group by 交易卡号
order by count(*) desc;

select *
from account
where 交易账号 = '3400022301204917165';

select
    交易户名,
    sum(交易金额) as total
from slip
where 收付标志 = '出'
group by 交易户名
order by total desc;

select
    交易户名,
    sum(交易金额) as total
from slip
where 收付标志 = '进'
group by 交易户名
order by total desc;

select
    sum(交易金额) as total
from slip
where 收付标志 = '出'
order by total desc;

select
    sum(交易金额) as total
from slip
where 收付标志 = '进'
order by total desc;

# 武汉珍伴网络科技有限公司
select *
from account
where 交易卡号 = '8888888252089840';


select *
from slip
where 交易户名 = '朱阳' and 收付标志 = '出';