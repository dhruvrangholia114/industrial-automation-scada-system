const $ = id => document.getElementById(id);
async function post(url, body={}) {
  const response = await fetch(url, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}
function render(s) {
  $("level").textContent = `${s.level}%`;
  $("sensorValue").textContent = `${s.level}%`;
  $("levelBar").style.width = `${s.level}%`;
  $("water").style.height = `${s.level}%`;
  $("pump").textContent = s.pump_on ? "RUNNING" : "STOPPED";
  $("pump").style.color = s.pump_on ? "#16834a" : "#667085";
  $("mode").textContent = s.mode;
  $("modeSelect").value = s.mode;
  $("plcBadge").textContent = s.plc_status;
  $("plcBadge").style.background = s.sensor_fault ? "#ffe2df" : "#d8f8e5";
  $("plcBadge").style.color = s.sensor_fault ? "#b42318" : "#146c43";
  $("alarmCount").textContent = s.alarms.length;
  $("fault").checked = s.sensor_fault;
  $("pumpOn").disabled = s.mode !== "MANUAL" || s.sensor_fault || s.level >= 95;
  $("pumpOff").disabled = s.mode !== "MANUAL";
  $("alarms").innerHTML = s.alarms.length ? s.alarms.map(a=>`<div class="alarm ${a.severity==="HIGH"?"high":""}"><b>${a.severity}</b> — ${a.message}${s.alarm_acknowledged?" <small>(acknowledged)</small>":""}</div>`).join("") : '<p class="muted">No active alarms.</p>';
}
async function refresh(){try{render(await (await fetch("/api/status")).json())}catch(e){$("plcBadge").textContent="OFFLINE"}}
$("modeSelect").addEventListener("change", async e=>{try{await post("/api/control",{mode:e.target.value});refresh()}catch(e){alert(e.message)}});
$("pumpOn").addEventListener("click",async()=>{await post("/api/control",{pump:true});refresh()});
$("pumpOff").addEventListener("click",async()=>{await post("/api/control",{pump:false});refresh()});
$("drain").addEventListener("click",async()=>{await post("/api/simulate",{drain:20});refresh()});
$("fill").addEventListener("click",async()=>{await post("/api/simulate",{fill:20});refresh()});
$("fault").addEventListener("change",async e=>{await post("/api/simulate",{sensor_fault:e.target.checked});refresh()});
$("ack").addEventListener("click",async()=>{await post("/api/acknowledge");refresh()});
refresh();setInterval(refresh,1000);
