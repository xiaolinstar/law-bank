create database if not exists bank;

CREATE TABLE IF NOT EXISTS bank_transactions (
    `交易卡号` VARCHAR(255) COMMENT '银行卡号',
    `交易账号` VARCHAR(255) COMMENT '银行账户号码',
    `查询反馈结果原因` VARCHAR(255) COMMENT '交易状态描述',
    `交易户名` VARCHAR(255) COMMENT '账户持有人姓名',
    `交易证件号码` VARCHAR(255) COMMENT '身份证/证件号码',
    `交易时间` DATETIME COMMENT '交易发生时间',
    `交易金额` DECIMAL(12,2) COMMENT '交易金额',
    `交易余额` DECIMAL(12,2) COMMENT '交易后账户余额',
    `收付标志` VARCHAR(10) COMMENT '出/进账标识',
    `交易对手账卡号` VARCHAR(255) COMMENT '对方账户/卡号',
    `现金标志` VARCHAR(10) COMMENT '现金/转账标识',
    `对手户名` VARCHAR(255) COMMENT '对方账户名称',
    `对手身份证号` VARCHAR(255) COMMENT '对方证件号码',
    `对手开户银行` VARCHAR(255) COMMENT '对方银行名称',
    `摘要说明` VARCHAR(255) COMMENT '交易摘要',
    `交易币种` CHAR(3) COMMENT '货币类型如CNY',
    `交易网点名称` VARCHAR(255) COMMENT '办理网点名称',
    `交易发生地` VARCHAR(255) COMMENT '交易发生地点',
    `交易是否成功` CHAR(2) COMMENT '01-成功 其他-失败',
    `传票号` VARCHAR(255),
    `IP地址` VARCHAR(45) COMMENT '交易终端IP',
    `MAC地址` VARCHAR(255) COMMENT '设备物理地址',
    `对手交易余额` DECIMAL(12,2) COMMENT '对方账户余额',
    `交易流水号` VARCHAR(255) PRIMARY KEY COMMENT '唯一流水号',
    `日志号` VARCHAR(255),
    `凭证种类` VARCHAR(255),
    `凭证号` VARCHAR(255),
    `交易柜员号` VARCHAR(255) COMMENT '柜员编号',
    `备注` TEXT,
    `商户名称` VARCHAR(255),
    `商户代码` VARCHAR(255),
    `交易类型` VARCHAR(255) COMMENT '消费/转账/充值等'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert into bank_transactions values (
'6212262314004721315','2314507101007709914','交易成功','','','2024-11-19 12:18:27',
                                      300.00,201.80,'出','243300133','现金交易',
                                      '深圳市财付通支付科技有限公司','','','正常','CNY',
                                      '工行四川省宜宾翠屏支行','快捷支付','01','','84.121.97.83','',NULL,
                                      '00000000667','','','','00236','','','','消费')
