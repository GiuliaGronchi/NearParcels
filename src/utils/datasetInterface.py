def get_data_interface(product_id='MEDSEA_MULTIYEAR_PHY_006_004'):
    
    if product_id == 'MEDSEA_MULTIYEAR_PHY_006_004':
        dict_ = {
            product_id : {
                'med-cmcc-tem-rean-d' : ['thetao'],
                'med-cmcc-cur-rean-d' : ['uo', 'vo'],
                'med-cmcc-sal-rean-d' : ['so']
                }
            }
    elif product_id == 'NWSHELF_MULTIYEAR_PHY_004_009':
         dict_ = {
            product_id : {
                'cmems_mod_nws_phy-t_my_7km-3D_P1D-m' : ['thetao'],
                'cmems_mod_nws_phy-uv_my_7km-3D_P1D-m' : ['uo', 'vo'],
                'cmems_mod_nws_phy-s_my_7km-3D_P1D-m' : ['so']
                }
            }
    else:
        print(f'ERROR in get_data_interface. Unrecognized product id: {product_id}')
        return
    
    return dict_