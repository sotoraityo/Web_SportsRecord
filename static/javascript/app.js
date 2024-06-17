document.addEventListener('DOMContentLoaded', function () {
    //カレンダーの要素を取得
    var calendarEl = document.getElementById('calendar');
    //カレンダーの要素にイベントを追加
    let calendar = new FullCalendar.Calendar(calendarEl, {
        //plugins: [interactionPlugin, dayGridPlugin],
        //初期設定
        initialView: "dayGridMonth",
        headerToolbar: {
            left: "",
            center: "title",
            right: "prev,next today",
        },
        locale: "ja",
        //ボタン設定
        buttonText: {
            today:    '今日',
            month:    '月',
            week:     '週',
            day:      '日'
        },
         // 週モード (fixed, liquid, variable)
         weekMode: 'fixed',
         // 週数を表示
         weekNumbers: false,
        
        
        dateClick: function(info) {
            //alert('Date: ' + info.dateStr);

            // form を動的に生成
            var form = document.createElement('form');
            form.action = '/create';
            form.method = 'POST';
      
            // body に追加
            document.body.append(form);
            //フォーム送信直前に、データをセットさせる
            form.addEventListener('formdata', (e) => {
                var fd = e.formData;
                // データをセット
                fd.set('select_date', info.dateStr);
              });    
  
            // submit
            form.submit();
        },
        //イベントの追加
        
        events: [
            {
                 title: '予定1',
                 start: '2023-10-15 10:00:00',
                 end: '2023-10-15 12:00:00',
            },
            {
                title: '予定2',
                start: '2023-10-17 21:00:00',
                end: '2023-10-18 02:00:00'
            },
            {
                title: '予定3',
                start: '2023-10-20',
                allDay: true
            },
            {
                title: '記入済み',
                start: datevalue,
                allDay: true
            }
            /*{% for ev in events %}
            {
                title: '{{ev.title}}',
                start:'{{ev.start}}',
            },
            {% endfor %}
            */
        
        ],


         // 選択可
         selectable: true,
         selectHelper: true,
         
 
    });  

    calendar.render();
});
