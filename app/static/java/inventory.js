window.addEventListener('load', function() 
{
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const campusSelect = document.getElementById('campus2');
        const banner=document.getElementById('banner-name').value;
        if(banner==="Inventory")
        {
            campusSelect.addEventListener('change', function() {
                inventoryRequest();
            });
        }
    }
});
function inventoryRequest()
{
    
}