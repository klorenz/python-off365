def parse_service_plans(s):
    sku = {}
    sku_by_string_id = {}
    plans = {}
    plan_by_string_id = {}

    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0:
            continue

        if "\t" in line:
            data = line.strip().split("\t")
            sku_item = {
                'productName': " ".join([ w.lower().capitalize() for w in data[0].split() ]),
                'stringId': data[1],
                'skuId': data[2],
                'availablePlans': {},
            }
            sku[data[2]] = sku_item
            sku_by_string_id[data[1]] = sku_item

            line = data[3]

        name, guid = line[:-1].split(" (")
        plan = {
            'stringId': name,
            'planId': guid,
        }
        sku_item['availablePlans'][guid] = plan
        plans[guid] = plan
        plan_by_string_id[name] = plan

    return {
        "skus": sku,
        "plans": plans,
        "skus_by_string_id": sku_by_string_id,
        "plans_by_string_id": plan_by_string_id
    }

#
# For updating this service plan file, please simply cut and paste rows from
# first table of:
#
# https://docs.microsoft.com/de-de/azure/active-directory/active-directory-licensing-product-and-service-plan-reference
#
SERVICE_PLANS = parse_service_plans("""
    AZURE ACTIVE DIRECTORY BASIC	AAD_BASIC	2b9c8e7c-319c-43a2-a2a0-48c5c6161de7	AAD_BASIC (c4da7f8a-5ee2-4c99-a7e1-87d2df57f6fe)
    AZURE ACTIVE DIRECTORY PREMIUM P1	AAD_PREMIUM	078d2b04-f1bd-4111-bbd4-b4b1b354cef4	AAD_PREMIUM (41781fb2-bc02-4b7c-bd55-b576c07bb09d)
        MFA_PREMIUM (8a256a2b-b617-496d-b51b-e76466e88db0)
    AZURE INFORMATION PROTECTION PLAN 1	RIGHTSMANAGEMENT	c52ea49f-fe5d-4e95-93ba-1de91d380f89	RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        RMS_S_PREMIUM (6c57d4b6-3b23-47a5-9bc9-69f17b4947b3)
    DYNAMICS 365 CUSTOMER ENGAGEMENT PLAN ENTERPRISE EDITION	DYN365_ENTERPRISE_PLAN1	ea126fc5-a19e-42e2-a731-da9d437bffcf	DYN365_ENTERPRISE_P1 (d56f3deb-50d8-465a-bedb-f079817ccac1)
        FLOW_DYN_P2 (b650d915-9886-424b-a08d-633cede56f57)
        NBENTERPRISE (03acaee3-9492-4f40-aed4-bcb6b32981b6)
        POWERAPPS_DYN_P2 (0b03f40b-c404-40c3-8651-2aceb74365fa)
        PROJECT_CLIENT_SUBSCRIPTION (fafd7243-e5c1-4a3a-9e40-495efcb1d3c3)
        SHAREPOINT_PROJECT (fe71d6c3-a2ea-4499-9778-da042bf08063)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    DYNAMICS 365 FOR FINANCIALS BUSINESS EDITION	DYN365_FINANCIALS_BUSINESS_SKU	cc13a803-544e-4464-b4e4-6d6169a138fa	DYN365_FINANCIALS_BUSINESS (920656a2-7dd8-4c83-97b6-a356414dbd36)
        FLOW_DYN_APPS (7e6d7d78-73de-46ba-83b1-6d25117334ba)
        POWERAPPS_DYN_APPS (874fc546-6efe-4d22-90b8-5c4e7aa59f4b)
    DYNAMICS 365 FOR SALES ENTERPRISE EDITION	DYN365_ENTERPRISE_SALES	1e1a282c-9c54-43a2-9310-98ef728faace	DYN365_ENTERPRISE_SALES (2da8e897-7791-486b-b08f-cc63c8129df7)
        FLOW_DYN_APPS (7e6d7d78-73de-46ba-83b1-6d25117334ba)
        NBENTERPRISE (03acaee3-9492-4f40-aed4-bcb6b32981b6)
        POWERAPPS_DYN_APPS (874fc546-6efe-4d22-90b8-5c4e7aa59f4b)
        PROJECT_ESSENTIALS (1259157c-8581-4875-bca7-2ffb18c51bda)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    DYNAMICS 365 FOR TEAM MEMBERS ENTERPRISE EDITION	DYN365_ENTERPRISE_TEAM_MEMBERS	8e7a3d30-d97d-43ab-837c-d7701cef83dc	DYN365_Enterprise_Talent_Attract_TeamMember (643d201a-9884-45be-962a-06ba97062e5e)
        DYN365_Enterprise_Talent_Onboard_TeamMember (f2f49eef-4b3f-4853-809a-a055c6103fe0)
        DYN365_ENTERPRISE_TEAM_MEMBERS (6a54b05e-4fab-40e7-9828-428db3b336fa)
        Dynamics_365_for_Operations_Team_members (f5aa7b45-8a36-4cd1-bc37-5d06dea98645)
        Dynamics_365_for_Retail_Team_members (c0454a3d-32b5-4740-b090-78c32f48f0ad)
        Dynamics_365_for_Talent_Team_members (d5156635-0704-4f66-8803-93258f8b2678)
        FLOW_DYN_TEAM (1ec58c70-f69c-486a-8109-4b87ce86e449)
        POWERAPPS_DYN_TEAM (52e619e2-2730-439a-b0d3-d09ab7e8b705)
        PROJECT_ESSENTIALS (1259157c-8581-4875-bca7-2ffb18c51bda)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    ENTERPRISE MOBILITY + SECURITY E3	EMS	efccb6f7-5641-4e0e-bd10-b4976e1bf68e	AAD_PREMIUM (41781fb2-bc02-4b7c-bd55-b576c07bb09d)
        ADALLOM_S_DISCOVERY (932ad362-64a8-4783-9106-97849a1a30b9)
        INTUNE_A (c1ec4a95-1f05-45b3-a911-aa3fa01094f5)
        MFA_PREMIUM (8a256a2b-b617-496d-b51b-e76466e88db0)
        RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        RMS_S_PREMIUM (6c57d4b6-3b23-47a5-9bc9-69f17b4947b3)
    ENTERPRISE MOBILITY + SECURITY E5	EMSPREMIUM	b05e124f-c7cc-45a0-a6aa-8cf78c946968	AAD_PREMIUM (41781fb2-bc02-4b7c-bd55-b576c07bb09d)
        AAD_PREMIUM_P2 (eec0eb4f-6444-4f95-aba0-50c24d67f998)
        ADALLOM_S_STANDALONE (2e2ddb96-6af9-4b1d-a3f0-d6ecfd22edb2)
        INTUNE_A (c1ec4a95-1f05-45b3-a911-aa3fa01094f5)
        MFA_PREMIUM (8a256a2b-b617-496d-b51b-e76466e88db0)
        RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        RMS_S_PREMIUM (6c57d4b6-3b23-47a5-9bc9-69f17b4947b3)
        RMS_S_PREMIUM2 (5689bec4-755d-4753-8b61-40975025187c)
    EXCHANGE ONLINE (PLAN 1)	EXCHANGESTANDARD	4b9405b0-7788-4568-add1-99614e613b69	EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
    EXCHANGE ONLINE (PLAN 2)	EXCHANGEENTERPRISE	19ec0d23-8335-4cbd-94ac-6050e30712fa	EXCHANGE_S_ENTERPRISE (efb87545-963c-4e0d-99df-69c6916d9eb0)
    EXCHANGE ONLINE ARCHIVING FOR EXCHANGE ONLINE	EXCHANGEARCHIVE_ADDON	ee02fd1b-340e-4a4b-b355-4a514e4c8943	EXCHANGE_S_ARCHIVE_ADDON (176a09a6-7ec5-4039-ac02-b2791c6ba793)
    EXCHANGE ONLINE ARCHIVING FOR EXCHANGE SERVER	EXCHANGEARCHIVE	90b5e015-709a-4b8b-b08e-3200f994494c	EXCHANGE_S_ARCHIVE (da040e0a-b393-4bea-bb76-928b3fa1cf5a)
    EXCHANGE ONLINE ESSENTIALS	EXCHANGEESSENTIALS	7fc0182e-d107-4556-8329-7caaa511197b	EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
    EXCHANGE ONLINE ESSENTIALS	EXCHANGE_S_ESSENTIALS	e8f81a67-bd96-4074-b108-cf193eb9433b	EXCHANGE_S_ESSENTIALS (1126bef5-da20-4f07-b45e-ad25d2581aa8)
    EXCHANGE ONLINE KIOSK	EXCHANGEDESKLESS	80b2d799-d2ba-4d2a-8842-fb0d0f3a4b82	EXCHANGE_S_DESKLESS (4a82b400-a79f-41a4-b4e2-e94f5787b113)
    INTUNE	INTUNE_A	061f9ace-7d42-4136-88ac-31dc755f143f	INTUNE_A (c1ec4a95-1f05-45b3-a911-aa3fa01094f5)
    MICROSOFT DYNAMICS CRM ONLINE BASIC	CRMPLAN2	906af65a-2970-46d5-9b58-4e9aa50f0657	CRMPLAN2 (bf36ca64-95c6-4918-9275-eb9f4ce2c04f)
        FLOW_DYN_APPS (7e6d7d78-73de-46ba-83b1-6d25117334ba)
        POWERAPPS_DYN_APPS (874fc546-6efe-4d22-90b8-5c4e7aa59f4b)
    MICROSOFT DYNAMICS CRM ONLINE PROFESSIONAL	CRMSTANDARD	d17b27af-3f49-4822-99f9-56a661538792	CRMSTANDARD (f9646fb2-e3b2-4309-95de-dc4833737456)
        FLOW_DYN_APPS (7e6d7d78-73de-46ba-83b1-6d25117334ba)
        MDM_SALES_COLLABORATION (3413916e-ee66-4071-be30-6f94d4adfeda)
        NBPROFESSIONALFORCRM (3e58e97c-9abe-ebab-cd5f-d543d1529634)
        POWERAPPS_DYN_APPS (874fc546-6efe-4d22-90b8-5c4e7aa59f4b)
    MICROSOFT INTUNE A DIRECT	INTUNE_A	061f9ace-7d42-4136-88ac-31dc755f143f	INTUNE_A (c1ec4a95-1f05-45b3-a911-aa3fa01094f5)
    MS IMAGINE ACADEMY	IT_ACADEMY_AD	ba9a34de-4489-469d-879c-0f0f145321cd	IT_ACADEMY_AD (d736def0-1fde-43f0-a5be-e3f8b2de6e41)
    OFFICE 365 BUSINESS	O365_BUSINESS	cdd28e44-67e3-425e-be4c-737fab2899d3	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        OFFICE_BUSINESS (094e7854-93fc-4d55-b2c0-3ab5369ebdc1)
        ONEDRIVESTANDARD (13696edf-5a08-49f6-8134-03083ed8ba30)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    OFFICE 365 BUSINESS	SMB_BUSINESS	b214fe43-f5a3-4703-beeb-fa97188220fc	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        OFFICE_BUSINESS (094e7854-93fc-4d55-b2c0-3ab5369ebdc1)
        ONEDRIVESTANDARD (13696edf-5a08-49f6-8134-03083ed8ba30)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    OFFICE 365 BUSINESS ESSENTIALS	O365_BUSINESS_ESSENTIALS	3b555118-da6a-4418-894f-7df1e2096870	EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
        FLOW_O365_P1 (0f9b09cb-62d1-4ff4-9129-43f4996f83f4)
        FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        POWERAPPS_O365_P1 (92f7a6f3-b89b-4bbd-8c30-809e6da5ad1c)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 BUSINESS ESSENTIALS	SMB_BUSINESS_ESSENTIALS	dab7782a-93b1-4074-8bb1-0e61318bea0b	EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
        FLOW_O365_P1 (0f9b09cb-62d1-4ff4-9129-43f4996f83f4)
        FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        POWERAPPS_O365_P1 (92f7a6f3-b89b-4bbd-8c30-809e6da5ad1c)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_MIDSIZE (41bf139a-4e60-409f-9346-a1361efc6dfb)
    OFFICE 365 BUSINESS PREMIUM	O365_BUSINESS_PREMIUM	f245ecc8-75af-4f8e-b61f-27d8114de5f3	EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
        FLOW_O365_P1 (0f9b09cb-62d1-4ff4-9129-43f4996f83f4)
        FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        MICROSOFTBOOKINGS (199a5c09-e0ca-4e37-8f7c-b05d533e1ea2)
        O365_SB_Relationship_Management (5bfe124c-bbdc-4494-8835-f1297d457d79)
        OFFICE_BUSINESS (094e7854-93fc-4d55-b2c0-3ab5369ebdc1)
        POWERAPPS_O365_P1 (92f7a6f3-b89b-4bbd-8c30-809e6da5ad1c)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 BUSINESS PREMIUM	SMB_BUSINESS_PREMIUM	ac5cef5d-921b-4f97-9ef3-c99076e5470f	EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
        FLOW_O365_P1 (0f9b09cb-62d1-4ff4-9129-43f4996f83f4)
        FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        MICROSOFTBOOKINGS (199a5c09-e0ca-4e37-8f7c-b05d533e1ea2)
        O365_SB_Relationship_Management (5bfe124c-bbdc-4494-8835-f1297d457d79)
        OFFICE_BUSINESS (094e7854-93fc-4d55-b2c0-3ab5369ebdc1)
        POWERAPPS_O365_P1 (92f7a6f3-b89b-4bbd-8c30-809e6da5ad1c)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_MIDSIZE (41bf139a-4e60-409f-9346-a1361efc6dfb)
    OFFICE 365 ENTERPRISE E1	STANDARDPACK	18181a46-0d4e-45cd-891e-60aabd171b4e	Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
        FLOW_O365_P1 (0f9b09cb-62d1-4ff4-9129-43f4996f83f4)
        FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        POWERAPPS_O365_P1 (92f7a6f3-b89b-4bbd-8c30-809e6da5ad1c)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_E1 (743dd19e-1ce3-4c62-a3ad-49ba8f63a2f6)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 ENTERPRISE E2	STANDARDWOFFPACK	6634e0ce-1a9f-428c-a498-f84ec7b8aa2e	Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EXCHANGE_S_STANDARD (9aaf7827-d63c-4b61-89c3-182f06f82e5c)
        FLOW_O365_P1 (0f9b09cb-62d1-4ff4-9129-43f4996f83f4)
        FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        POWERAPPS_O365_P1 (92f7a6f3-b89b-4bbd-8c30-809e6da5ad1c)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_E1 (743dd19e-1ce3-4c62-a3ad-49ba8f63a2f6)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 ENTERPRISE E3	ENTERPRISEPACK	6fd2c87f-b296-42f0-b197-1e91e994b900	Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EXCHANGE_S_ENTERPRISE (efb87545-963c-4e0d-99df-69c6916d9eb0)
        FLOW_O365_P2 (76846ad7-7776-4c40-a281-a386362dd1b9)
        FORMS_PLAN_E3 (2789c901-c14e-48ab-a76a-be334d9d793a)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        POWERAPPS_O365_P2 (c68f8d98-5534-41c8-bf36-22fa496fa792)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_E3 (9e700747-8b1d-45e5-ab8d-ef187ceec156)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 ENTERPRISE E3 DEVELOPER	DEVELOPERPACK	189a915c-fe4f-4ffa-bde4-85b9628d07a0	EXCHANGE_S_ENTERPRISE (efb87545-963c-4e0d-99df-69c6916d9eb0)
        FLOW_O365_P2 (76846ad7-7776-4c40-a281-a386362dd1b9)
        FORMS_PLAN_E5 (e212cbc7-0961-4c40-9825-01117710dcb1)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        POWERAPPS_O365_P2 (c68f8d98-5534-41c8-bf36-22fa496fa792)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        SHAREPOINT_S_DEVELOPER (a361d6e2-509e-4e25-a8ad-950060064ef4)
        SHAREPOINTWAC_DEVELOPER (527f7cdd-0e86-4c47-b879-f5fd357a3ac6)
        STREAM_O365_E5 (6c6042f5-6f01-4d67-b8c1-eb99d36eed3e)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
    OFFICE 365 ENTERPRISE E4	ENTERPRISEWITHSCAL	1392051d-0cb9-4b7a-88d5-621fee5e8711	Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EXCHANGE_S_ENTERPRISE (efb87545-963c-4e0d-99df-69c6916d9eb0)
        FLOW_O365_P2 (76846ad7-7776-4c40-a281-a386362dd1b9)
        FORMS_PLAN_E3 (2789c901-c14e-48ab-a76a-be334d9d793a)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        MCOVOICECONF (27216c54-caf8-4d0d-97e2-517afb5c08f6)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        POWERAPPS_O365_P2 (c68f8d98-5534-41c8-bf36-22fa496fa792)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_E3 (9e700747-8b1d-45e5-ab8d-ef187ceec156)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 ENTERPRISE E5	ENTERPRISEPREMIUM	c7df2760-2c81-4ef7-b578-5b5392b571df	ADALLOM_S_O365 (8c098270-9dd4-4350-9b30-ba4703f3b36b)
        BI_AZURE_P2 (70d33638-9c74-4d01-bfd3-562de28bd4ba)
        Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EQUIVIO_ANALYTICS (4de31727-a228-4ec3-a5bf-8e45b5ca48cc)
        EXCHANGE_ANALYTICS (34c0d7a0-a70f-4668-9238-47f9fc208882)
        EXCHANGE_S_ENTERPRISE (efb87545-963c-4e0d-99df-69c6916d9eb0)
        FLOW_O365_P3 (07699545-9485-468e-95b6-2fca3738be01)
        FORMS_PLAN_E5 (e212cbc7-0961-4c40-9825-01117710dcb1)
        LOCKBOX_ENTERPRISE (9f431833-0334-42de-a7dc-70aa40db46db)
        MCOEV (4828c8ec-dc2e-4779-b502-87ac9ce28ab7)
        MCOMEETADV (3e26ee1f-8a5f-4d52-aee2-b81ce45c8f40)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        POWERAPPS_O365_P3 (9c0dab89-a30c-4117-86e7-97bda240acd2)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_E5 (6c6042f5-6f01-4d67-b8c1-eb99d36eed3e)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        THREAT_INTELLIGENCE (8e0c0a52-6a6c-4d40-8370-dd62790dcd70)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 ENTERPRISE E5 WITHOUT PSTN CONFERENCING	ENTERPRISEPREMIUM_NOPSTNCONF	26d45bd9-adf1-46cd-a9e1-51e9a5524128	ADALLOM_S_O365 (8c098270-9dd4-4350-9b30-ba4703f3b36b)
        BI_AZURE_P2 (70d33638-9c74-4d01-bfd3-562de28bd4ba)
        Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EQUIVIO_ANALYTICS (4de31727-a228-4ec3-a5bf-8e45b5ca48cc)
        EXCHANGE_ANALYTICS (34c0d7a0-a70f-4668-9238-47f9fc208882)
        EXCHANGE_S_ENTERPRISE (efb87545-963c-4e0d-99df-69c6916d9eb0)
        FLOW_O365_P3 (07699545-9485-468e-95b6-2fca3738be01)
        FORMS_PLAN_E5 (e212cbc7-0961-4c40-9825-01117710dcb1)
        LOCKBOX_ENTERPRISE (9f431833-0334-42de-a7dc-70aa40db46db)
        MCOEV (4828c8ec-dc2e-4779-b502-87ac9ce28ab7)
        MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        POWERAPPS_O365_P3 (9c0dab89-a30c-4117-86e7-97bda240acd2)
        PROJECTWORKMANAGEMENT (b737dad2-2f6c-4c65-90e3-ca563267e8b9)
        RMS_S_ENTERPRISE (bea4c11e-220a-4e6d-8eb8-8ea15d019f90)
        SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_E5 (6c6042f5-6f01-4d67-b8c1-eb99d36eed3e)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        THREAT_INTELLIGENCE (8e0c0a52-6a6c-4d40-8370-dd62790dcd70)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 F1	DESKLESSPACK	4b585984-651b-448a-9e53-3b10f069cf7f	Deskless (8c7d2df8-86f0-4902-b2ed-a0458298f3b3)
        EXCHANGE_S_DESKLESS (4a82b400-a79f-41a4-b4e2-e94f5787b113)
        FLOW_O365_S1 (bd91b1a4-9f94-4ecf-b45b-3a65e5c8128a)
        FORMS_PLAN_K (f07046bd-2a3c-4b96-b0be-dea79d7cbfb8)
        MCOIMP (afc06cb0-b4f4-4473-8286-d644f70d8faf)
        POWERAPPS_O365_S1 (e0287f9f-e222-4f98-9a83-f379e249159a)
        SHAREPOINTDESKLESS (902b47e5-dcb2-4fdc-858b-c63a90a2bdb9)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        STREAM_O365_K (3ffba0d2-38e5-4d5e-8ec0-98f2b05c09d9)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        TEAMS1 (57ff2da0-773e-42df-b2af-ffb7a2317929)
        YAMMER_ENTERPRISE (7547a3fe-08ee-4ccb-b430-5077c5041653)
    OFFICE 365 MIDSIZE BUSINESS	MIDSIZEPACK	04a7fb0d-32e0-4241-b4f5-3f7618cd1162	EXCHANGE_S_STANDARD_MIDMARKET (fc52cc4b-ed7d-472d-bbe7-b081c23ecc56)
        MCOSTANDARD_MIDMARKET (b2669e95-76ef-4e7e-a367-002f60a39f3e)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        SHAREPOINTENTERPRISE_MIDMARKET (6b5b6a67-fc72-4a1f-a2b5-beecf05de761)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
        YAMMER_MIDSIZE (41bf139a-4e60-409f-9346-a1361efc6dfb)
    OFFICE 365 PROPLUS	OFFICESUBSCRIPTION	c2273bd0-dff7-4215-9ef5-2c7bcfb06425	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
        OFFICESUBSCRIPTION (43de0ff5-c92c-492b-9116-175376d08c38)
        ONEDRIVESTANDARD (13696edf-5a08-49f6-8134-03083ed8ba30)
        SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    OFFICE 365 SMALL BUSINESS	LITEPACK	bd09678e-b83c-4d3f-aaba-3dad4abd128b	EXCHANGE_L_STANDARD (d42bdbd6-c335-4231-ab3d-c8f348d5aff5)
        MCOLITE (70710b6b-3ab4-4a38-9f6d-9f169461650a)
        SHAREPOINTLITE (a1f3d0a8-84c0-4ae0-bae4-685917b8ab48)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    OFFICE 365 SMALL BUSINESS PREMIUM	LITEPACK_P2	fc14ec4a-4169-49a4-a51e-2c852931814b	EXCHANGE_L_STANDARD (d42bdbd6-c335-4231-ab3d-c8f348d5aff5)
        MCOLITE (70710b6b-3ab4-4a38-9f6d-9f169461650a)
        OFFICE_PRO_PLUS_SUBSCRIPTION_SMBIZ (8ca59559-e2ca-470b-b7dd-afd8c0dee963)
        SHAREPOINTLITE (a1f3d0a8-84c0-4ae0-bae4-685917b8ab48)
        SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    ONEDRIVE FOR BUSINESS (PLAN 1)	WACONEDRIVESTANDARD	e6778190-713e-4e4f-9119-8b8238de25df	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
    ONEDRIVESTANDARD (13696edf-5a08-49f6-8134-03083ed8ba30)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    ONEDRIVE FOR BUSINESS (PLAN 2)	WACONEDRIVEENTERPRISE	ed01faf2-1d88-4947-ae91-45ca18703a96	ONEDRIVEENTERPRISE (afcafa6a-d966-4462-918c-ec0b4e0fe642)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    POWER BI FOR OFFICE 365 ADD-ON	POWER_BI_ADDON	45bc2c81-6072-436a-9b0b-3b12eefbc402	BI_AZURE_P1 (2125cfd7-2110-4567-83c4-c1cd5275163d)
    SQL_IS_SSIM (fc0a60aa-feee-4746-a0e3-aecfe81a38dd)
    POWER BI PRO	POWER_BI_PRO	f8a1db68-be16-40ed-86d5-cb42ce701560	BI_AZURE_P2 (70d33638-9c74-4d01-bfd3-562de28bd4ba)
    PROJECT FOR OFFICE 365	PROJECTCLIENT	a10d5e58-74da-4312-95c8-76be4e5b75a0	PROJECT_CLIENT_SUBSCRIPTION (fafd7243-e5c1-4a3a-9e40-495efcb1d3c3)
    PROJECT ONLINE ESSENTIALS	PROJECTESSENTIALS	776df282-9fc0-4862-99e2-70e561b9909e	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
    PROJECT_ESSENTIALS (1259157c-8581-4875-bca7-2ffb18c51bda)
    SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    PROJECT ONLINE PREMIUM	PROJECTPREMIUM	09015f9f-377f-4538-bbb5-f75ceb09358a	PROJECT_CLIENT_SUBSCRIPTION (fafd7243-e5c1-4a3a-9e40-495efcb1d3c3)
    SHAREPOINT_PROJECT (fe71d6c3-a2ea-4499-9778-da042bf08063)
    SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    PROJECT ONLINE PREMIUM WITHOUT PROJECT CLIENT	PROJECTONLINE_PLAN_1	2db84718-652c-47a7-860c-f10d8abbdae3	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
    SHAREPOINT_PROJECT (fe71d6c3-a2ea-4499-9778-da042bf08063)
    SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    PROJECT ONLINE PROFESSIONAL	PROJECTPROFESSIONAL	53818b1b-4a27-454b-8896-0dba576410e6	PROJECT_CLIENT_SUBSCRIPTION (fafd7243-e5c1-4a3a-9e40-495efcb1d3c3)
    SHAREPOINT_PROJECT (fe71d6c3-a2ea-4499-9778-da042bf08063)
    SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    PROJECT ONLINE WITH PROJECT FOR OFFICE 365	PROJECTONLINE_PLAN_2	f82a60b8-1ee3-4cfb-a4fe-1c6a53c2656c	FORMS_PLAN_E1 (159f4cd6-e380-449f-a816-af1a9ef76344)
    PROJECT_CLIENT_SUBSCRIPTION (fafd7243-e5c1-4a3a-9e40-495efcb1d3c3)
    SHAREPOINT_PROJECT (fe71d6c3-a2ea-4499-9778-da042bf08063)
    SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
    SHAREPOINTWAC (e95bec33-7c88-4a70-8e19-b10bd9d0c014)
    SWAY (a23b959c-7ce8-4e57-9140-b90eb88a9e97)
    SHAREPOINT ONLINE (PLAN 1)	SHAREPOINTSTANDARD	1fc08a02-8b3d-43b9-831e-f76859e04e1a	SHAREPOINTSTANDARD (c7699d2e-19aa-44de-8edf-1736da088ca1)
    SHAREPOINT ONLINE (PLAN 2)	SHAREPOINTENTERPRISE	a9732ec9-17d9-494c-a51c-d6b45b384dcb	SHAREPOINTENTERPRISE (5dbe027f-2339-4123-9542-606e4d348a72)
    SKYPE FOR BUSINESS CLOUD PBX	MCOEV	e43b5b99-8dfb-405f-9987-dc307f34bcbd	MCOEV (4828c8ec-dc2e-4779-b502-87ac9ce28ab7)
    SKYPE FOR BUSINESS ONLINE (PLAN 1)	MCOIMP	b8b749f8-a4ef-4887-9539-c95b1eaa5db7	MCOIMP (afc06cb0-b4f4-4473-8286-d644f70d8faf)
    SKYPE FOR BUSINESS ONLINE (PLAN 2)	MCOSTANDARD	d42c793f-6c78-4f43-92ca-e8f6a02b035f	MCOSTANDARD (0feaeb32-d00e-4d66-bd5a-43b5b83db82c)
    SKYPE FOR BUSINESS PSTN CONFERENCING	MCOMEETADV	0c266dff-15dd-4b49-8397-2bb16070ed52	MCOMEETADV (3e26ee1f-8a5f-4d52-aee2-b81ce45c8f40)
    SKYPE FOR BUSINESS PSTN DOMESTIC AND INTERNATIONAL CALLING	MCOPSTN2	d3b4fe1f-9992-4930-8acb-ca6ec609365e	MCOPSTN2 (5a10155d-f5c1-411a-a8ec-e99aae125390)
    SKYPE FOR BUSINESS PSTN DOMESTIC CALLING	MCOPSTN1	0dab259f-bf13-4952-b7f8-7db8f131b28d	MCOPSTN1 (4ed3ff63-69d7-4fb7-b984-5aec7f605ca8)
    VISIO PRO FOR OFFICE 365	VISIOCLIENT	c5928f49-12ba-48f7-ada3-0d743a3601d5	VISIO_CLIENT_SUBSCRIPTION (663a804f-1c30-4ff0-9915-9db84f0d1cea)
    WINDOWS 10 ENTERPRISE E3	WIN10_PRO_ENT_SUB	cb10e6cd-9da4-4992-867b-67546b1db821	WIN10_PRO_ENT_SUB (21b439ba-a0ca-424f-a6cc-52f954a5b111)
""")
