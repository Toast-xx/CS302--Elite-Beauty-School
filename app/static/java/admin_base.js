window.addEventListener('load', function() 
{

});
function section(id)
{
    const targets = document.querySelectorAll('.section');
    filter(id);
    document.getElementById('content').style.display='block';
    document.getElementById('add_product').style.display='none';
    targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
      document.getElementById('banner-name').textContent=id;
    }});
}
function filter(id)
{
  const admin=document.getElementById('superstatus');
  if(admin.checked)
    {
      document.getElementById('campus').style.display='flex';
      document.getElementById('campus2').style.display='flex';
    }
  else
    {
      document.getElementById('campus').style.display='none';
      document.getElementById('campus2').style.display='none';
    };
  if(id=='Orders'||id=='Dashboard')
  {
    document.getElementById('filter-order').style.display='flex';
    document.getElementById('filter-search').style.display='none';
  }
  else
  {
    document.getElementById('filter-order').style.display='none';
    document.getElementById('filter-search').style.display='inline-flex';
    document.getElementById('secondFilter').style.display='flex';
      document.getElementById('addProduct').style.display='flex';
    if(id=="Users")
    {
      document.getElementById('secondFilter').style.display='none';
    }
    if(id=="Inventory")
    {
      document.getElementById('addProduct').style.display='none';
    }
  }
}
function submitFilter()
{
  const start=document.getElementById('startdate');
  const end=document.getElementById('enddate');
  const banner=document.getElementById('banner-name').value;
  if(start.value>end.value)
  {
    alert("Please select the correct date range!");
    return;
  }
  if (banner=='Dashboard')
  {
    dashboardRequest();
  }
  else
  {
    ordersRequest();
  }
}