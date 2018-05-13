#!/usr/bin/env python3

TITLE = "Уцелевший терминал"

STATEMENT = '''
Совсем недавно произошло нечто совсем не поддающееся объяснению.

Под метровым слоем радиоактивного мусора наши разведчики обнаружили старинный терминал,
когда-то использовавшийся для доступа к серверам, связанным с системой управления.

Cамым удивительным было то, что когда мусор немного расчистили, из-под завалов начал пробиваться свет.
Терминал продолжал работать даже спустя три года после катастрофы.
На экране отображалась страница входа и её адрес:

[terminal.contest.qctf.ru/{0}/](https://terminal.contest.qctf.ru/{0}/).

В течение получаса мы тщетно пытались найти способ войти в систему, но всё было напрасно. 

Ни о каком способе узнать пароль не могло быть и речи: большинство документов, связанных с этими терминалами
было уничтожено, а те немногие, что остались — засекречены. Получить же доступ хотелось: ведь если сервера
всё ещё работают, мы сможем получить контроль над значительной частью сохранившихся объектов...
'''

task_ids = ['0f499640b143169fa2b013cccb314246', '5726682f9b98e9b6da552d481e15ea6c', '5cfd0f0552a0634b1976a751e7c61d54', '9e5574a4cc96626a2f2d902d9a2e6038', 'bd638da8799d67426c40adba988920f9', '2d0ef29c75ad76be57494d2490ffbed8', '339ee33c0376953a087e4e0129dbfc95', '5f3049c8318f6c9c7182007c7bdd9698', '04d6866cec2bcb9bfde99ec3665b838f', '3f9c26cf545402af82d84740222abe62', '081a3e5478714cc96b7c70b065e22bba', '65fdc0f3a3ca14482382aeccc5d743d9', '15adba114deb1f398a94d332de33d448', 'd33b41862a0f402713107e8cd2dac6c9', '7e9a2f374815aa19eae2263e11dc0edd', 'd58942537bc06694cd797be6625ee4d8', '0afb7c8db0018ac0215a15108d913060', 'b7c664b44a839435e9809434157b721d', 'ebb5a83e1222890e4849d18ef80c91b3', '7fbed5ab8cbd4b93a914ae357c7844e5', '72ce139b7a8087fced639a8610952be1', 'ad018625a53c78f0697dca81758e3559', 'bebbc6797e2d306e4d9fd735e5a764bb', 'eb62a367e9885c7d1fce7303d83687d3', '62a6c0fd97615ee4121316e86674166c', '20b2419a109f5894a6e4424f4d7c21c4', '50ad1de250d7454c62d931f985c0be61', '97a0547a43bc7fb518c66fcc3077ac90', '452c3c81852dafb9de80a70742f4bf0a', '414ca505564ac3e6d3fd17c2076b1201', '6b676be466fd12f4ff2245c968eee7bc', 'dae04dcaa7b06fad13ff4158f4882ad4', '4956c28df400b4ca1762a853e5be81d0', 'e1b817e0e16238b6cef6d317016ca670', '11fb4332d6900669cf46486e25273249', '77d652627f7c7a1ad73fbed19a05e6fa', 'db70d749a081faba5772bb0519c3562e', 'b2d9c4fa17b057da0e49bb5479496490', '35a046ae43d8caaa1710a3be03adedbf', 'ee22628b2a71daa492f928e2d4736ee8', 'a9ac13325c3d4e73b57282d3d3ca54d2', 'b2e80f5ece1defb00f8ab657ae174b79', '53e66e90120c6bedf0f4cea93fb3d079', 'fa90610ccb24477c9995de1cfc2fbca7', 'e85aa3eb9447fa05aa38f954075a09c2', 'f4f66246e5745e065c1736ac906e7018', '7f3b62be72186df97c5ef3d0cbf6572d', '365a9513fd97e3cdecf29094417c0103', '42a8652cdb8d54c709c09ba2c46d9001', 'f8f56c50e32e6d98cea36802bbbc26cc', 'c6417de26f9bda7794ad08643231b401', '155bc7ed00ae3ebc2b5e470653910657', '8777290072d0c94943c8e58810c45fc4', 'e0fe212bcd26ae0406dbed16f1fc1285', '0334db8d664e553bf93cc73212b4a0b1', 'c1f8de54bd5f27e8864887297a245143', '90c8d8ed247e75b8ab892896f5b1a31d', '27a136b5c030c121e602c3b4891c3786', 'b03b3212337e40989cf6156a5ece5171', '7da9a7174819dc9435aff308827bb340', 'ad19812c00920f950300f1cfcb46197b', 'ff67ba125d475d746538508875751e04', '2ec83bff0e69dead585b34e9cfd68b91', 'c805404f355bb2c4611f8e95046c7f0d', '189a6c62bba1b28dcad49ec9b48a45ae', 'c58769f574e4684e41eb435b2305390d', 'd320e87e75c1a72c1c126d78f1d3031f', 'f8203c834e595122225387f60b2fff71', 'e723c8d0e76c875e49ccbe91f2cba85c', 'f0ab1ec7f806eda11baadd0cb1047bcd', 'b4d7753362dbed37c6c0a21c396847a6', '99fd2da6c1607154b802a3b86058e47b', '69cd8ef1959508631381633c9f878c09', 'c24d76ab5d8e4a1e2d79c35f03be3048', '22728fca826ceaae496677019e44e973', '9363a5a97ad2042a978ad1966152791c', '58e08b1698cbcd1922e0dc65089ff91e', '615013ccdb8f9be23e4629a367667792', '801e14b7703103065149a0d72f06fe10', 'aad742276798aab61fcd398735d308d9', 'b1f2d08367b95476488569f6cd1b7c68', '0903bb74698c0cbcfbbdec512aa848ae', '5fcf1aa1b4c651ab7e77255a063d7153', 'f180edfceb770dc94aad7fccf8717fb5', 'a64e52300a3892b17a5c6e9dd4a6a9dc', '917acf54abe1895e940fed68132c4530', '34309cc2e4b570e48bf827b2132ff7c0', '3b7e4997c570d94590e97ac84fcaee26', '1a5cc396bc7204556eb5d2648da612fc', 'bb5aad631461bad7178b80b22045c7be', '5450eaa056de9e2b98497b0c76074f5b', '7fd430494d518dd6235a0a5d041661a8', '6189d06060527a10b5f38ac8afdb7897', 'ba26c9c62f2ff03d03b7d0822a7d5b84', '719f652eb8fa3db6926e304d53b4d52d', 'ffed01a8a19e5e90c501d94b75609ffa', 'cffc7bd2094995a05e660986527b694d', '2e9a78f0f8e926cfcdd27958646bc5b9', '2fcf06bbc0647879b9ef751cc01cc5f6', 'b70cb2b75e36c56f533bc8bdb176a7ed', 'f6c630ca29b984f268a3ea6180f9848d', 'f4acdd5cb6b4e148985690d40dc9fb9f', '81303e14a81ff35030126c11cdf3ac7b', '2c3d070bc72c2e5f75fcaa364a92bb2b', 'ccfc1b6ac16a848ef626562d83a30097', 'd80c9b78cab7d46c22ef015aa8d98ce8', '61d6641aa1b5b8dd4511e89a0c490b43', '5bd0e71e0919d914128737ebe6345c2c', '7b088c66ff7f3881a4faa99980b94168', 'bb35656903a7fbc9063adb079499b41a', 'e74788eefc87505b6c001274239b3389', '034359002470cb65ea454a12af6c3d26', '5fcf41a4d52972b965d722f036f598d0', '2deaa4ca41f6a88aeddeab588d19f2c4', 'c71d8919c5c2d7be8e5b4ef1bcc5bd8e', '1a597f59a48bf49873cebc5d1a0666be', '79da9cc10a7ff7d81c737e95d4a8211c', '839eb5f23af410bd3c179886c7eb9408', 'f3f950fc567da32df49753f176bc2274', 'a0678927d0ba0c5d699d55495dc65ec7', 'ec476821eebdba92bde427bf2bfee62e', 'a2089f8adf01641e3aabd20bd8088c72', 'f0a745d61efb7171370a82b2ca74e5d0', 'c146da0acd1086335a1f7692c0a96b52', '75e917850333f1a7fc762a77141370a2', '70dee03b978306f0965a49451562544d', 'c36b48e11a64fbfa69041957d8ae9386', '6ac343d3c3ed49dee27866df68f7002f', '4bd6ef04b4a327f5be79d574def90ff6', '0af274cffdcace603ca41cff4601d0cf', '99032325fc1f094ab9e9d019e48428e0', 'd9b446a6a32608e0a30501f07ead923d', 'c83be1722dd98abe713105f239e51224', '87c1950e9b285002b0e2bf87b0335d48', '14acd8ef6241efbef0a4252496b2701f', '9873e81eb1e47c14a474aee2af524bda', '3a436362a828e00abf030cac8503001e', 'ec0cfa58cdd55356bb68f42aa9933ca8', 'b31d1986de1683f13576addf3175dca6', 'dc112635fd677e56198c7b54b13a9b6e', 'a9481d29bd03d1861099eb2f0ea53a40', 'ac665b6556e7cb9e516bf4c20278b00e', '6ccc6bd88c51d76ced28951b7957f269', 'fd537de16049422f9de0f0515afaae81', '23072e40a6f33d54288f65a254e6177d', 'caf91aac61f267c32819c5779351e976', 'b040952d71457651db9d960522c9ebf8', '14fd6a488fdb962441c0644b5d312aa9', '0a60237e5ccc6af9ea06bc341f08e46f', '9b501f6145991e71b913c3ae013bfc54', '557aeb7a7784bd2bb468eaa7c743a8b4', '1a21e05bef25a0926272ca2721a67a56', '4f5fd33e6b072ab70d1a1cd9e89adb85', '6f606b91239282f649f37c3ff19d153f', '6c2244c0f52076518f9698c3d804088c', 'aa484eabfe6727db046ee89f2d385e0e', '5032d48da27d9fc64c92d0831d8ce3d0', '2c53e53457bd480cddb820f0f81b6b8e', '604451359e905b0eaeae29c67b3c5486', '3fbc7983e89afd77fd586e17e61127f0', '695b304b9861616791a88183b9843b1d', '68824e36c2d10779657f3009f152c45a', 'e24ce9c8aee12978769bd91201802182', '1eedbcceb5fb3315e2efe91435bd8d55', '38b5cd4fd86503b70b241cfeb960920f', '64680bf08d77682e05578989786fffaa', '58fde4a9b8a5f8cc8a51509946ac40a6', 'ed0ac55596835b7ec3632f9574159d29', 'd5042ebcb1ec4cf6c90490bbdaa20d74', '3280716802091009fb3556a732704d7c', '544bb6b2023367ed3fa0491808f44f7e', '19bbe59afb4500797a1239e044285e1c', '7fabb78ecd3374339c6c747df5396f68', '1cad408acd46311dbf8ceaed5bfd5496', 'e567053bfd0db30aa5f7adf884216604', '61bd9c4c1f0497e4fa7645318733b3b4', '3d6f9eb6328f83f02b1f2224ab19ed8f', '3c12a5d5e80b36378448671e3cb9096a', 'df00f636c923b15337cb185bb9f7cbe3', '1915d8eb09e85cef82a7b545b17e2698', 'a9cf8464335dc52bcfcaf6dec712a965', 'c8cdd2cda739ecd4ef7ca07fc71431e5', '07091def61c7104e0d8f33ef7bfe98d6', 'f8012f6c9a1a495060b4b4c7005e1b28', '5a663bc54e3a433bfca45e8aea8c9fe1', 'f179da0b18c617e123a4bef15ae56c60', '315fd763c00b180f649a9396580f0bc8', '1bdb109d6d5fe70c665ca7b5185bf115', 'aac46e2a14f29396067d0b83db3ebc65', '3d5402888fe6d88a1d593f7664492252', 'bd696b862038e8a44958ace52e7eb552', '6cb5460a4feb2b1bb155962e7488d59f', 'eab330ca9fb7812067f8e625926c5a4b', '098c9cd4efc209a559cfc0af7e4ab1b2', '07671f92c6ca77bced0ddc4fa1db9bcb', '70b4367fd90b8325f05231f43e868abc', '45f7b9651a9ad2a53a468f45c25bdea9', '380302821b83801d3f2013b8763246fb', 'd9ada672b3b1f3058624f45f0a095f7c', '224cbcf08513090f72b575bdcd513fa0']


def generate(context):
    participant = context['participant']

    task_id = task_ids[participant.id % len(task_ids)]

    return TaskStatement(TITLE, STATEMENT.format(task_id))