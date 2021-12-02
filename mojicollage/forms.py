from django import forms

from mojicollage.widgets import RangeInput

class createInfo(forms.Form):
    tgtImg = forms.ImageField(label="画像を選択")
    myName = forms.CharField(label="自分の名前（呼ばれかた）（任意）", required=False, max_length=20)
    myAge = forms.IntegerField(label="自分の年齢（任意）", required=False)
    tgtName = forms.CharField(label="女の子の名前（任意）", required=False, max_length=20)
    tgtAge = forms.IntegerField(label="女の子の年齢（任意）", required=False)
    tgtSeikaku = forms.IntegerField(label="女の子の性格", min_value=1, max_value=5, widget=RangeInput)
    tgtKeigo = forms.ChoiceField(
        label="女の子の話し方",
        choices = (
            ('0', 'ため口'),
            ('1', '敬語')
        ),
        widget=forms.widgets.RadioSelect
    )
    finish = forms.ChoiceField(
        label="射精",
        choices = (
            ('0', 'おまかせ'),
            ('1', '我慢する'),
            ('2', '限界。。')
        ),
        widget=forms.widgets.RadioSelect
    )
