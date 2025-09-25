# Identifying Red Hat components using CPEs
Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications,
operating systems, and hardware devices present among an enterprise's computing assets.

Red Hat uses CPEs to uniquely identify each product and version, following the CPE 2.2 schema.

## RHEL 10 CPEs
Starting with  RHEL 10, we will change the way CPEs are assigned to RHEL:

* Minor versions will be used in CPEs for mainstream RHEL versions
* The `cpe:/o` prefix will be used instead of mixed usage of `cpe:/o` and `cpe:/a` for all RHEL variants
* The channel specifiers are being dropped


### Minor Version CPEs
Previously, for RHEL 9 and earlier we assigned generic CPEs like `cpe:/o:redhat:enterprise_linux:9` for the entire 
lifetime of a major release. Minor versions were only reflected in xUS CPEs (e.g., `cpe:/a:redhat:rhel_eus:9.2::appstream`).

Starting with RHEL 10 and all following versions of RHEL, we will use minor versions in mainstream CPEs, 
e.g., `cpe:/o:redhat:enterprise_linux:10.0`, incrementing with each subsequent minor release. This will apply to the 
MAIN, GA, and MAIN.EUS variants. This makes it easier to determine which version of RHEL an advisory was released for 
without consulting ET product configuration. This also improves our way of tracking releases and which sets of 
advisories they shipped. More granular minor versions also allow for the use of version ranges later on, which can be 
used to sets of versions (without having to enumerate them all) where the security status such as "fixed" is applicable.

### CPE Type Standardization
Previously, we used a mix of `cpe:/o` (operating system) and `cpe:/a` (application) for different variants of RHEL 
(for example, base OS used o and Appstream used a). It is unclear why we decided on this different usage and we've 
encountered various issues in our security data files where consumers have to account for both prefixes even though 
they identify the same products.

Starting with RHEL 10 and all following versions of RHEL, we will standardize on `cpe:/o` for all RHEL-related components
(those shipped under the RHEL product in Errata Tool). EUS CPEs will also transition from `cpe:/a` to `cpe:/o`, for example:
Base OS: `cpe:/o:redhat:enterprise_linux_eus:10.2`
AppStream: `cpe:/o:redhat:enterprise_linux_eus:10.2`

### Removal of channel specifiers and consistent naming of EUS CPEs
CPEs for RHEL 9 and earlier used channel specifiers such as `::appstream` and `::baseos` to differentiate between different
Errata Tool Variants and pin a specific CPE to a set of RPM repositories. These specifiers were never used externally
by any vendor or any of our external documents for any reason other than arbitrary differentiation between groups of
content. Starting with RHEL 10, we will drop the use of channel specifiers for RHEL. We will continue using them for
layered products to distinguish their base RHEL version if known.

Extended streams such as EUS, AUS or TUS always used the name rhel instead of enterprise_linux in the CPE name.
Starting with RHEL 10, we will use enterprise_linux only for increased consistency.




