window.weiqi = new Vue({
    el: '#weiqi',
    data: {
        qipan: [[]],
        status: '',
        score1: 0,
        score2: 0,
        outText: ''
    },
    methods: {
        reflushQiPan: function () {
            var bg = document.getElementById('chessboard');
            bg.innerHTML = "";
            for (var i = 0; i < this.qipan.length; i++) {
                line = this.qipan[i];
                for (var j = 0; j < line.length; j++) {
                    point = line[j];
                    if (point != 0) {
                        var div = document.createElement('div');
                        div.className = 'chess';
                        div.style.left = (i - 0.5) + "rem";
                        div.style.top = (j - 0.5) + "rem";

                        div.style.background = "#EEE";
                        if (point == 1) {
                            div.style.background = "#000";
                        }
                        bg.appendChild(div);
                    } else {
                        var btn = document.createElement('button');
                        btn.style.position = 'absolute';
                        btn.style.height = '0.95rem';
                        btn.style.width = '0.95rem';
                        btn.style.left = (i - 0.5) + "rem";
                        btn.style.top = (j - 0.5) + "rem";

                        btn.style.background = "transparent";
                        btn.style['border-style'] = "none";
                        btn.style['border-outline'] = "none";
                        btn.x = i;
                        btn.y = j;
                        btn.onclick = function () {
                            window.weiqi.do(this.x, this.y);
                        }
                        bg.appendChild(btn);
                    }
                }
            }
        },
        start: function () {
            this.$http.get('http://192.168.40.62:8088/start').then(response => response.json()).then(json => {
                this.status = json['status'];
                this.score1 = json['score1'];
                this.score2 = json['score2'];
                this.qipan = json['qipan'];
                this.reflushQiPan();
            }, function () {
                this.outText = '请求失败处理';
            });

        },
        do: function (x, y) {
            if (this.status == 'turn1' || this.status == 'turn2') {
                var data = { "x": x, "y": y }
                this.$http.post('http://192.168.40.62:8088/do', data).then(response => response.json()).then(json => {
                    this.status = json['status'];
                    this.score1 = json['score1'];
                    this.score2 = json['score2'];
                    this.qipan = json['qipan'];
                    this.reflushQiPan();
                }, function (res) {
                    this.outText = '请求失败处理';
                });
            }
        }
    }
})