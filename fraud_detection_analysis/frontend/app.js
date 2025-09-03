const API="http://localhost:8000";

async function metrics(){
  let r=await fetch(API+"/metrics"); let j=await r.json();
  document.getElementById("k_total").innerText=j.total;
  document.getElementById("k_flagged").innerText=j.flagged;
}

async function loadTable(){
  let r=await fetch(API+"/transactions?limit=50"); let data=await r.json();
  $('#txTable').DataTable({
    data:data,destroy:true,
    columns:[
      {title:"ID",data:"transaction_id"},
      {title:"Customer",data:"customer_id"},
      {title:"City",data:"city"},
      {title:"Merchant",data:"merchant_category"},
      {title:"Amount",data:"amount"},
      {title:"Status",data:"is_fraud",render:d=>d==1?"Suspicious":"Normal"}
    ]
  });
}

metrics(); loadTable();
